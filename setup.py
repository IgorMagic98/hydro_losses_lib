from setuptools import setup, find_packages

setup(
    name="hydro_losses_lib",
    version="0.1.0",
    description="Библиотека для расчета гидравлических потерь в гидравлических элементах",
    author="Igor Shepovalov",
    author_email="shepovalov.igor@mail.ru",
    packages=find_packages(),
    python_requires=">=3.6",
)