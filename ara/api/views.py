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

from rest_framework import viewsets

from ara.api import models, serializers


class LabelViewSet(viewsets.ModelViewSet):
    queryset = models.Label.objects.all()
    serializer_class = serializers.LabelSerializer


class PlaybookViewSet(viewsets.ModelViewSet):
    queryset = models.Playbook.objects.all()
    serializer_class = serializers.PlaybookSerializer
    filter_fields = ("name", "status")


class PlayViewSet(viewsets.ModelViewSet):
    queryset = models.Play.objects.all()
    serializer_class = serializers.PlaySerializer
    filter_fields = ("playbook", "uuid")


class TaskViewSet(viewsets.ModelViewSet):
    queryset = models.Task.objects.all()
    serializer_class = serializers.TaskSerializer
    filter_fields = ("playbook",)


class HostViewSet(viewsets.ModelViewSet):
    queryset = models.Host.objects.all()
    serializer_class = serializers.HostSerializer
    filter_fields = ("playbook",)


class ResultViewSet(viewsets.ModelViewSet):
    queryset = models.Result.objects.all()
    serializer_class = serializers.ResultSerializer
    filter_fields = ("playbook", "status")


class FileViewSet(viewsets.ModelViewSet):
    queryset = models.File.objects.all()
    serializer_class = serializers.FileSerializer
    filter_fields = ("playbook", "path")


class RecordViewSet(viewsets.ModelViewSet):
    queryset = models.Record.objects.all()
    serializer_class = serializers.RecordSerializer
    filter_fields = ("playbook", "key")


class StatsViewSet(viewsets.ModelViewSet):
    queryset = models.Stats.objects.all()
    serializer_class = serializers.StatsSerializer
    filter_fields = ("playbook", "host")
