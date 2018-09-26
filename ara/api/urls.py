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

from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from ara.api import views

urlpatterns = [
    path('', views.api_root),
    path('labels', views.LabelList.as_view(), name='label-list'),
    path('labels/<int:pk>', views.LabelDetail.as_view(), name='label-detail'),
    path('playbooks', views.PlaybookList.as_view(), name='playbook-list'),
    path('playbooks/<int:pk>', views.PlaybookDetail.as_view(), name='playbook-detail'),
    path('playbooks/<int:pk>/files', views.PlaybookFilesDetail.as_view(), name='playbook-file-detail'),
    path('plays', views.PlayList.as_view(), name='play-list'),
    path('plays/<int:pk>', views.PlayDetail.as_view(), name='play-detail'),
    path('tasks', views.TaskList.as_view(), name='task-list'),
    path('tasks/<int:pk>', views.TaskDetail.as_view(), name='task-detail'),
    path('hosts', views.HostList.as_view(), name='host-list'),
    path('hosts/<int:pk>', views.HostDetail.as_view(), name='host-detail'),
    path('results', views.ResultList.as_view(), name='result-list'),
    path('results/<int:pk>', views.ResultDetail.as_view(), name='result-detail'),
    path('files', views.FileList.as_view(), name='file-list'),
    path('files/<int:pk>', views.FileDetail.as_view(), name='file-detail'),
    path('stats', views.StatsList.as_view(), name='stats-list'),
    path('stats/<int:pk>', views.StatsDetail.as_view(), name='stats-detail'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
