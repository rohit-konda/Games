from setuptools import setup, find_packages

setup(name='Games',
      version='1.0',
      description='python package for defining various types of games',
      URL='-',
      author='-',
      author_email='-',
      license='None',
      packages=find_packages(),
      install_requires=[
          'numpy', 'cvxopt', 'scipy', 'matplotlib'],
      classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
      ],
      zip_safe=False)
