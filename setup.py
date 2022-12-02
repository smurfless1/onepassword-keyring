from setuptools import setup

setup(
    name='onepassword-keyring',
    packages=['onepassword_keyring'],
    install_requires=[
        'keyring',
        'onepassword>=2.0.0'
    ],
    entry_points={
        'keyring.backends': [
            'onepassword = onepassword_keyring',
        ]
    },
)
