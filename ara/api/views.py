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
import sys

import pbr.version
from rest_framework import viewsets
from rest_framework.response import Response

from ara.api import models, serializers


class InfoView(viewsets.ViewSet):
    def list(self, request):
        return Response(
            {
                "python_version": ".".join(map(str, sys.version_info[:3])),
                "ara_version": pbr.version.VersionInfo("ara-server").release_string(),
            }
        )


class LabelViewSet(viewsets.ModelViewSet):
    queryset = models.Label.objects.all()

    def get_serializer_class(self):
        if self.action in ["create", "update", "destroy"]:
            return serializers.LabelSerializer
        if self.action in ["list", "retrieve"]:
            return serializers.ListLabelSerializer
        return serializers.LabelSerializer


class PlaybookViewSet(viewsets.ModelViewSet):
    queryset = models.Playbook.objects.all()
    filter_fields = ("name", "status")

    def get_serializer_class(self):
        if self.action in ["create", "update", "destroy"]:
            return serializers.PlaybookSerializer
        if self.action in ["list", "retrieve"]:
            return serializers.ListPlaybookSerializer
        return serializers.PlaybookSerializer


class PlayViewSet(viewsets.ModelViewSet):
    queryset = models.Play.objects.all()
    filter_fields = ("playbook", "uuid")

    def get_serializer_class(self):
        if self.action in ["create", "update", "destroy"]:
            return serializers.PlaySerializer
        if self.action in ["list", "retrieve"]:
            return serializers.ListPlaySerializer
        return serializers.PlaySerializer


class TaskViewSet(viewsets.ModelViewSet):
    queryset = models.Task.objects.all()
    filter_fields = ("playbook",)

    def get_serializer_class(self):
        if self.action in ["create", "update", "destroy"]:
            return serializers.TaskSerializer
        if self.action in ["list", "retrieve"]:
            return serializers.ListTaskSerializer
        return serializers.TaskSerializer


class HostViewSet(viewsets.ModelViewSet):
    queryset = models.Host.objects.all()
    filter_fields = ("playbook",)

    def get_serializer_class(self):
        if self.action in ["create", "update", "destroy"]:
            return serializers.HostSerializer
        if self.action in ["list", "retrieve"]:
            return serializers.ListHostSerializer
        return serializers.HostSerializer


class ResultViewSet(viewsets.ModelViewSet):
    filter_fields = ("playbook",)

    def get_queryset(self):
        statuses = self.request.GET.getlist("status")
        if statuses:
            return models.Result.objects.filter(status__in=statuses)
        return models.Result.objects.all()

    def get_serializer_class(self):
        if self.action in ["create", "update", "destroy"]:
            return serializers.ResultSerializer
        if self.action in ["list", "retrieve"]:
            return serializers.ListResultSerializer
        return serializers.ResultSerializer


class FileViewSet(viewsets.ModelViewSet):
    queryset = models.File.objects.all()
    filter_fields = ("playbook", "path")

    def get_serializer_class(self):
        if self.action in ["create", "update", "destroy"]:
            return serializers.FileSerializer
        if self.action in ["list", "retrieve"]:
            return serializers.ListFileSerializer
        return serializers.FileSerializer


class RecordViewSet(viewsets.ModelViewSet):
    queryset = models.Record.objects.all()
    filter_fields = ("playbook", "key")

    def get_serializer_class(self):
        if self.action in ["create", "update", "destroy"]:
            return serializers.RecordSerializer
        if self.action in ["list", "retrieve"]:
            return serializers.ListRecordSerializer
        return serializers.RecordSerializer


class StatsViewSet(viewsets.ModelViewSet):
    queryset = models.Stats.objects.all()
    filter_fields = ("playbook", "host")

    def get_serializer_class(self):
        if self.action in ["create", "update", "destroy"]:
            return serializers.StatsSerializer
        if self.action in ["list", "retrieve"]:
            return serializers.ListStatsSerializer
        return serializers.StatsSerializer
