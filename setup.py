# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['onepassword_keyring']

package_data = \
{'': ['*']}

install_requires = \
['keyring>=23.11.0,<24.0.0', 'onepassword>=2.0.1,<3.0.0']

entry_points = \
{'keyring.backends': ['onepassword = onepassword_keyring']}

setup_kwargs = {
    'name': 'onepassword-keyring',
    'version': '2.0.9',
    'description': 'keyring wrapper for onepassword module',
    'long_description': 'None',
    'author': 'David Brown',
    'author_email': 'forums@smurfless.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

