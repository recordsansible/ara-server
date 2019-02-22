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

from rest_framework import serializers

from ara.api import fields as ara_fields, models


class SimpleLabelSerializer(serializers.ModelSerializer):
    """
    Simple label serializer used in lists or for displaying relationships
    """

    class Meta:
        model = models.Label
        fields = ("id", "name")


class SimplePlaybookSerializer(serializers.ModelSerializer):
    """
    Simple playbook serializer used in lists or for displaying relationships
    """

    class Meta:
        model = models.Playbook
        fields = ("id", "name", "path")


class SimplePlaySerializer(serializers.ModelSerializer):
    """
    Simple play serializer used in lists or for displaying relationships
    """

    class Meta:
        model = models.Play
        fields = ("id", "name")


class SimpleTaskSerializer(serializers.ModelSerializer):
    """
    Simple task serializer used in lists or for displaying relationships
    """

    class Meta:
        model = models.Task
        fields = ("id", "name")


class SimpleHostSerializer(serializers.ModelSerializer):
    """
    Simple host serializer used in lists or for displaying relationships
    """

    class Meta:
        model = models.Host
        fields = ("id", "name", "alias")


class SimpleResultSerializer(serializers.ModelSerializer):
    """
    Simple result serializer used in lists or for displaying relationships
    """

    class Meta:
        model = models.Result
        fields = ("id", "status")


class SimpleFileSerializer(serializers.ModelSerializer):
    """
    Simple file serializer used in lists or for displaying relationships
    """

    class Meta:
        model = models.File
        fields = ("id", "path")


class SimpleRecordSerializer(serializers.ModelSerializer):
    """
    Simple record serializer used in lists or for displaying relationships
    """

    class Meta:
        model = models.Record
        fields = ("id", "key")


class DurationSerializer(serializers.ModelSerializer):
    """
    Serializer for objects that occur over a period of time and have a duration.
    """

    class Meta:
        abstract = True

    duration = serializers.SerializerMethodField()

    @staticmethod
    def get_duration(obj):
        if obj.ended is None:
            return obj.updated - obj.started
        return obj.ended - obj.started


class LabelSerializer(serializers.ModelSerializer):
    """
    Default serializer for labels
    """

    class Meta:
        model = models.Label
        fields = "__all__"

    description = ara_fields.CompressedTextField(
        default=ara_fields.EMPTY_STRING, help_text="A text description of the label"
    )


class PlaybookSerializer(DurationSerializer):
    """
    Default serializer for playbooks
    """

    class Meta:
        model = models.Playbook
        fields = "__all__"

    arguments = ara_fields.CompressedObjectField(default=ara_fields.EMPTY_DICT)
    labels = LabelSerializer(many=True, default=[])

    def create(self, validated_data):
        # First create the playbook without the labels
        labels = validated_data.pop("labels")
        playbook = models.Playbook.objects.create(**validated_data)

        # Now associate the labels to the playbook
        for label in labels:
            playbook.labels.add(models.Label.objects.create(**label))

        return playbook


class PlaySerializer(DurationSerializer):
    """
    Default serializer for plays
    """

    class Meta:
        model = models.Play
        fields = "__all__"


class TaskSerializer(DurationSerializer):
    """
    Default serializer for tasks
    """

    class Meta:
        model = models.Task
        fields = "__all__"

    tags = ara_fields.CompressedObjectField(default=ara_fields.EMPTY_LIST, help_text="A list containing Ansible tags")


class HostSerializer(serializers.ModelSerializer):
    """
    Default serializer for hosts
    """

    class Meta:
        model = models.Host
        fields = "__all__"

    facts = ara_fields.CompressedObjectField(default=ara_fields.EMPTY_DICT)

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


class ResultSerializer(DurationSerializer):
    """
    Default serializer for results
    """

    class Meta:
        model = models.Result
        fields = "__all__"

    content = ara_fields.CompressedObjectField(default=ara_fields.EMPTY_DICT)


class FileSerializer(serializers.ModelSerializer):
    """
    Default serializer for files
    """

    class Meta:
        model = models.File
        fields = "__all__"

    sha1 = serializers.SerializerMethodField()
    content = ara_fields.FileContentField()

    @staticmethod
    def get_sha1(obj):
        return obj.content.sha1


class RecordSerializer(serializers.ModelSerializer):
    """
    Default Serializer for records
    """

    class Meta:
        model = models.Record
        fields = "__all__"

    value = ara_fields.CompressedObjectField(
        default=ara_fields.EMPTY_STRING, help_text="A string, list, dict, json or other formatted data"
    )


class StatsSerializer(serializers.ModelSerializer):
    """
    Default Serializer for stats
    """

    class Meta:
        model = models.Stats
        fields = "__all__"


class ListLabelSerializer(serializers.ModelSerializer):
    """
    Serializer for listing labels and their relationships
    """

    class Meta:
        model = models.Label
        fields = "__all__"

    description = ara_fields.CompressedTextField(
        default=ara_fields.EMPTY_STRING, help_text="A text description of the label"
    )


class ListPlaybookSerializer(DurationSerializer):
    """
    Serializer for listing playbooks and their relationships
    """

    class Meta:
        model = models.Playbook
        fields = "__all__"

    arguments = ara_fields.CompressedObjectField(read_only=True)
    labels = SimpleLabelSerializer(many=True, read_only=True, default=[])
    plays = SimplePlaySerializer(many=True, read_only=True, default=[])
    tasks = SimpleTaskSerializer(many=True, read_only=True, default=[])
    hosts = SimpleHostSerializer(many=True, read_only=True, default=[])
    results = SimpleResultSerializer(many=True, read_only=True, default=[])
    files = SimpleFileSerializer(many=True, read_only=True, default=[])
    records = SimpleRecordSerializer(many=True, read_only=True, default=[])


class ListPlaySerializer(DurationSerializer):
    """
    Serializer for listing plays and their relationships
    """

    class Meta:
        model = models.Play
        fields = "__all__"

    playbook = SimplePlaybookSerializer(read_only=True)
    hosts = SimpleHostSerializer(many=True, read_only=True, default=[])
    tasks = SimpleTaskSerializer(many=True, read_only=True, default=[])
    results = SimpleResultSerializer(many=True, read_only=True, default=[])


class ListTaskSerializer(DurationSerializer):
    """
    Serializer for listing tasks and their relationships
    """

    class Meta:
        model = models.Task
        fields = "__all__"

    tags = ara_fields.CompressedObjectField(read_only=True)
    results = SimpleResultSerializer(many=True, read_only=True, default=[])


class ListHostSerializer(serializers.ModelSerializer):
    """
    Serializer for listing hosts and their relationships
    """

    class Meta:
        model = models.Host
        exclude = ("facts",)

    playbook = SimplePlaybookSerializer(read_only=True)


class ListResultSerializer(DurationSerializer):
    """
    Serializer for listing results and their relationships
    """

    class Meta:
        model = models.Result
        exclude = ("content",)

    playbook = SimplePlaybookSerializer(read_only=True)
    play = SimplePlaySerializer(read_only=True)
    task = SimpleTaskSerializer(read_only=True)
    host = SimpleHostSerializer(read_only=True)


class ListFileSerializer(serializers.ModelSerializer):
    """
    Serializer for listing files and their relationships
    """

    class Meta:
        model = models.File
        exclude = ("content",)

    playbook = SimplePlaybookSerializer(read_only=True)


class ListRecordSerializer(serializers.ModelSerializer):
    """
    Serializer for listing records and their relationships
    """

    class Meta:
        model = models.Record
        exclude = ("value",)

    playbook = SimplePlaybookSerializer(read_only=True)


class ListStatsSerializer(serializers.ModelSerializer):
    """
    Serializer for listing stats and their relationships
    """

    class Meta:
        model = models.Stats
        fields = "__all__"

    playbook = SimplePlaybookSerializer(read_only=True)
    host = SimpleHostSerializer(read_only=True)
