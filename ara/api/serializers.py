#  Copyright (c) 2018 Red Hat, Inc.
#
#  This file is part of ARA Records Ansible.
#
#  ARA is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  ARA is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with ARA.  If not, see <http://www.gnu.org/licenses/>.

import hashlib
import json
import logging
import zlib

from rest_framework import serializers

from ara.api import models

DATE_FORMAT = "(iso-8601: 2016-05-06T17:20:25.749489-04:00)"
DURATION_FORMAT = "([DD] [HH:[MM:]]ss[.uuuuuu])"
logger = logging.getLogger("ara.api.serializers")


class DurationMixin(object):
    """
    Provides a method for retrieving the duration of an object with
    "started", "updated" and "ended" timestamps.
    """
    def get_duration(self, obj):
        if obj.ended is None:
            return obj.updated - obj.started
        return obj.ended - obj.started


class CompressedTextField(serializers.CharField):
    """
    Compresses text before storing it in the database.
    Decompresses text from the database before serving it.
    """

    def to_representation(self, obj):
        return zlib.decompress(obj).decode("utf8")

    def to_internal_value(self, data):
        return zlib.compress(data.encode("utf8"))


class CompressedObjectField(serializers.JSONField):
    """
    Serializes/compresses an object (i.e, list, dict) before storing it in the
    database.
    Decompresses/deserializes an object before serving it.
    """

    def to_representation(self, obj):
        return json.loads(zlib.decompress(obj).decode("utf8"))

    def to_internal_value(self, data):
        return zlib.compress(json.dumps(data).encode("utf8"))


class FileContentField(serializers.CharField):
    """
    Compresses text before storing it in the database.
    Decompresses text from the database before serving it.
    """

    def to_representation(self, obj):
        return zlib.decompress(obj.contents).decode("utf8")

    def to_internal_value(self, data):
        contents = data.encode("utf8")
        sha1 = hashlib.sha1(contents).hexdigest()
        content_file, created = models.FileContent.objects.get_or_create(
            sha1=sha1, defaults={"sha1": sha1, "contents": zlib.compress(contents)}
        )
        return content_file


class FileContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FileContent
        fields = "__all__"


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.File
        fields = "__all__"

    sha1 = serializers.SerializerMethodField()
    content = FileContentField()

    @staticmethod
    def get_sha1(obj):
        return obj.content.sha1


class HostSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Host
        fields = "__all__"

    facts = CompressedObjectField(default=zlib.compress(json.dumps({}).encode("utf8")))

    def get_unique_together_validators(self):
        """
        Hosts have a "unique together" constraint for host.name and play.id.
        We want to have a "get_or_create" facility and in order to do that, we
        must manage the validation during the creation, not before.
        Overriding this method effectively disables this validator.
        """
        return []

    def create(self, validated_data):
        host, created = models.Host.objects.get_or_create(
            name=validated_data["name"], playbook=validated_data["playbook"], defaults=validated_data
        )
        return host


class ResultSerializer(serializers.ModelSerializer, DurationMixin):
    class Meta:
        model = models.Result
        fields = "__all__"

    duration = serializers.SerializerMethodField()
    content = CompressedObjectField(default=zlib.compress(json.dumps({}).encode("utf8")))


class LabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Label
        fields = "__all__"

    description = CompressedTextField(
        default=zlib.compress(json.dumps("").encode("utf8")), help_text="A textual description of the label"
    )


class TaskSerializer(serializers.ModelSerializer, DurationMixin):
    class Meta:
        model = models.Task
        fields = "__all__"

    duration = serializers.SerializerMethodField()
    tags = CompressedObjectField(
        default=zlib.compress(json.dumps([]).encode("utf8")), help_text="A JSON list containing Ansible tags"
    )


class SimpleTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Task
        fields = ("id", "name")


class RecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Record
        fields = "__all__"

    value = CompressedObjectField(
        default=zlib.compress(json.dumps("").encode("utf8")),
        help_text="A string, list, dict, json or other formatted data",
    )


class PlaySerializer(serializers.ModelSerializer, DurationMixin):
    class Meta:
        model = models.Play
        fields = "__all__"

    duration = serializers.SerializerMethodField()
    hosts = HostSerializer(read_only=True, many=True)
    results = ResultSerializer(read_only=True, many=True)


class SimplePlaySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Play
        fields = "__all__"


class StatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Stats
        fields = "__all__"


class PlaybookSerializer(serializers.ModelSerializer, DurationMixin):
    class Meta:
        model = models.Playbook
        fields = "__all__"

    duration = serializers.SerializerMethodField()
    arguments = CompressedObjectField(default=zlib.compress(json.dumps({}).encode("utf8")))
    files = FileSerializer(many=True, default=[])
    hosts = HostSerializer(many=True, default=[])
    labels = LabelSerializer(many=True, default=[])
    tasks = SimpleTaskSerializer(many=True, read_only=True, default=[])
    plays = SimplePlaySerializer(many=True, read_only=True, default=[])
    records = RecordSerializer(many=True, read_only=True, default=[])

    def create(self, validated_data):
        # Create the playbook without the file and label references for now
        files = validated_data.pop("files")
        hosts = validated_data.pop("hosts")
        labels = validated_data.pop("labels")
        playbook = models.Playbook.objects.create(**validated_data)

        # Add the files, hosts and the labels in
        for file_ in files:
            playbook.hosts.add(models.File.objects.create(**file_))
        for host in hosts:
            playbook.hosts.add(models.Host.objects.create(**host))
        for label in labels:
            playbook.labels.add(models.Label.objects.create(**label))

        return playbook
