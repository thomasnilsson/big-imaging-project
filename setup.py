import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
        name='bigimg2019',  
        version='0.9',
        scripts=['bigimg2019'] ,
        author="Thomas Nilsson",
        author_email="tnni@dtu.dk",
        description="A compilation of functions for Big Imaging 2019",
        long_description=long_description,
        long_description_content_type="text/markdown",
        url="https://github.com/thomasnilsson/big-imaging-project",
        packages=setuptools.find_packages(),
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ]
)