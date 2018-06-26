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

from rest_framework.test import APITestCase

from ara.api import models, serializers
from ara.api.tests import factories
from ara.api.tests import utils


class HostTestCase(APITestCase):
    def test_host_factory(self):
        host = factories.HostFactory(name='testhost')
        self.assertEqual(host.name, 'testhost')

    def test_host_serializer(self):
        play = factories.PlayFactory()
        serializer = serializers.HostSerializer(data={
            'name': 'serializer',
            'play': play.id
        })
        serializer.is_valid()
        host = serializer.save()
        host.refresh_from_db()
        self.assertEqual(host.name, 'serializer')
        self.assertEqual(host.play.id, play.id)

    def test_host_serializer_compress_facts(self):
        play = factories.PlayFactory()
        serializer = serializers.HostSerializer(data={
            'name': 'compress',
            'facts': factories.HOST_FACTS,
            'play': play.id,
        })
        serializer.is_valid()
        host = serializer.save()
        host.refresh_from_db()
        self.assertEqual(host.facts, utils.compressed_obj(factories.HOST_FACTS))

    def test_host_serializer_decompress_facts(self):
        host = factories.HostFactory(
            facts=utils.compressed_obj(factories.HOST_FACTS)
        )
        serializer = serializers.HostSerializer(instance=host)
        self.assertEqual(serializer.data['facts'], factories.HOST_FACTS)

    def test_get_no_hosts(self):
        request = self.client.get('/api/v1/hosts')
        self.assertEqual(0, len(request.data['results']))

    def test_get_hosts(self):
        host = factories.HostFactory()
        request = self.client.get('/api/v1/hosts')
        self.assertEqual(1, len(request.data['results']))
        self.assertEqual(host.name, request.data['results'][0]['name'])

    def test_delete_host(self):
        host = factories.HostFactory()
        self.assertEqual(1, models.Host.objects.all().count())
        request = self.client.delete('/api/v1/hosts/%s' % host.id)
        self.assertEqual(204, request.status_code)
        self.assertEqual(0, models.Host.objects.all().count())

    def test_create_host(self):
        play = factories.PlayFactory()
        self.assertEqual(0, models.Host.objects.count())
        request = self.client.post('/api/v1/hosts', {
            'name': 'create',
            'play': play.id
        })
        self.assertEqual(201, request.status_code)
        self.assertEqual(1, models.Host.objects.count())

    def test_post_same_host_for_a_play(self):
        play = factories.PlayFactory()
        self.assertEqual(0, models.Host.objects.count())
        request = self.client.post('/api/v1/hosts/', {
            'name': 'create',
            'play': play.id,
            'ok': 1
        })
        self.assertEqual(201, request.status_code)
        self.assertEqual(1, models.Host.objects.count())
        self.assertEqual(1, request.data['ok'])

        request = self.client.post('/api/v1/hosts/', {
            'name': 'create',
            'play': play.id,
            'ok': 2
        })
        self.assertEqual(201, request.status_code)
        self.assertEqual(1, models.Host.objects.count())
        # This isn't expected to update the count for 'ok', it's not a patch
        self.assertEqual(1, request.data['ok'])

    def test_partial_update_host(self):
        host = factories.HostFactory()
        self.assertNotEqual(1, host.ok)
        request = self.client.patch('/api/v1/hosts/%s' % host.id, {
            'ok': 1
        })
        self.assertEqual(200, request.status_code)
        host_updated = models.Host.objects.get(id=host.id)
        self.assertEqual(1, host_updated.ok)

    def test_get_host(self):
        host = factories.HostFactory()
        request = self.client.get('/api/v1/hosts/%s' % host.id)
        self.assertEqual(host.name, request.data['name'])
