from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()

setup(name='openmindat',
      version='0.0.6',
      description='An alpha version for OpenMindat package',
      long_description=open('README.md').read(),
      long_description_content_type='text/markdown',
      classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: Apache Software License',
        "Programming Language :: Python :: 3",
        'Programming Language :: Python :: 3.10',
        "Topic :: Software Development :: Libraries :: Python Modules",
    	"Topic :: Scientific/Engineering :: Information Analysis",
      ],
      keywords='mindat openmindat mineral data python api',
      url='https://github.com/ChuBL/OpenMindat',
      author='Jiyin Zhang',
      author_email='jiyinz@uidaho.edu',
      license='Apache Software License',
      packages=['openmindat'],
      install_requires=[
          'requests',
          'PyYAML',
          'tqdm'
      ],
      include_package_data=True,
      zip_safe=False)