# -*- coding:utf-8 -*-
"""
@author: fsksf

@since: 2022/1/12 16:37
"""
from setuptools import Extension, setup, find_packages

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()


setup(
    name='vnpy_qmt',  # Required
    version='0.2.0',  # Required
    description='vnpy qmt gateway',  # Required
    long_description=long_description,  # Optional
    long_description_content_type='text/markdown',  # Optional (see note above)
    url="https://github.com/fsksf/vnpy_qmt",
    author='fsksf',  # Optional
    author_email='kangyuqiang123@qq.com',
    classifiers=[  # Optional
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3.7',
    ],
    keywords='vnpy gateway qmt',  # Optional
    packages=find_packages()
)
