
import setuptools
with open('README.md', 'r', encoding='utf-8') as readme_file:
    long_description = readme_file.read()

with open('LEIAME.md', 'r', encoding='utf-8') as readme_file:
    long_description_PTBR = readme_file.read()

setuptools.setup(
    name = "dadosgov-JOSEGOIS",
    version = "1",
    author="José Henrique Targino Dias Gois",
    author_email="josegoismail@gmail.com",
    description="Interface with dados.gov.br",
    long_description = long_description,
    long_description_content_type="text/markdown",
    url="https://"

)
