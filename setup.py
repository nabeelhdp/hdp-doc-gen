#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) Nabeel Moidu
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy of
# the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.

from setuptools import setup, find_packages

long_description = ("Collects cluster configuration information,"
                    "Component specific settings,"
                    "host + role combinations,"
                    "versions etc from Ambari via REST API and"
                    "produces output in form of "
                    "Confluence friendly HTML page."
                    )

setup(
    name='hdp-doc-gen',
    version='0.1',
    author=u'Nabeel Moidu',
    author_email='nmoidu@cloudera.com',
    description='Generate Confluence documentation page for HDP cluster',
    long_description=long_description,
    url='http://github.com/nabeelhdp/hdp-doc-gen',
    packages=find_packages(
        include=['hdp-doc-gen'],
        exclude=['*.tests', '*.tests.*', 'tests.*', 'tests']
    ),
    python_requires='>=3.0',
    license='Apache License 2.0',
    keywords='HDP Documentation Cluster'.split(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Topic :: Utilities',
        'Programming Language :: Python',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS',
        "Topic :: Software Development :: Documentation",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
    ]
)
