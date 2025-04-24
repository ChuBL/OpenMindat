from setuptools import setup

with open('README.md') as f:
    long_description = f.read()

setup(name='openmindat',
      version='0.1.0',
      description='An alpha version for OpenMindat package',
      long_description=long_description,
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