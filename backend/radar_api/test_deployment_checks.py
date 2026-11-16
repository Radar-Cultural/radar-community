from django.core.checks import Warning
from django.test import SimpleTestCase

from radar_api.deployment_checks import unexpected_issues


class DeploymentCheckGateTests(SimpleTestCase):
    def test_allows_only_the_two_deferred_hsts_warnings(self):
        deferred = [
            Warning('HSTS subdominios', id='security.W005'),
            Warning('HSTS precarga', id='security.W021'),
        ]
        self.assertEqual(unexpected_issues(deferred), [])

        new_warning = Warning('Otro aviso de seguridad', id='security.W999')
        self.assertEqual(unexpected_issues([*deferred, new_warning]), [new_warning])
