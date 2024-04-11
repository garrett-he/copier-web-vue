import random

from chance import chance
from pytest_copie.plugin import Copie

LICENSE_SPEC = {
    'Apache-2.0': {'filename': 'LICENSE', 'stub': 'Apache License', 'with_holder': False},
    'BSD-3-Clause': {'filename': 'LICENSE', 'stub': 'BSD 3-Clause License', 'with_holder': True},
    'GPL-3.0-or-later': {'filename': 'COPYING', 'stub': 'GNU General Public License', 'with_holder': False},
    'LGPL-3.0-or-later': {'filename': 'COPYING', 'stub': 'GNU Lesser General Public License', 'with_holder': False},
    'MIT': {'filename': 'LICENSE', 'stub': 'MIT License', 'with_holder': True},
    'MPL-2.0': {'filename': 'LICENSE', 'stub': 'Mozilla Public License', 'with_holder': False},
    'Unlicense': {'filename': 'UNLICENSE', 'stub': 'This is free and unencumbered software released into the public domain', 'with_holder': False}
}


def generate_copier_answers():
    return {
        'project_name': f'{chance.word()}-{chance.word()}',
        'project_description': chance.sentence(),
        'project_version': f'{random.randint(0, 10)}.{random.randint(0, 10)}.{random.randint(0, 10)}',
        'project_keywords': f'{chance.word()},{chance.word()},{chance.word()}',
        'copyright_holder_name': chance.name(),
        'copyright_holder_email': chance.email(),
        'copyright_license': chance.pickone(list(LICENSE_SPEC.keys())),
        'copyright_year': str(random.randint(2000, 2024)),
        'vcs_github_path': f'{chance.word()}/{chance.word()}-{chance.word()}'.lower(),
    }


def get_license_file(license_id: str) -> str:
    match license_id:
        case 'GPL-3.0-or-later' | 'LGPL-3.0-or-later':
            return 'COPYING'
        case 'Unlicense':
            return 'UNLICENSE'
        case _:
            return 'LICENSE'


def test_template_static_files(copie: Copie):
    result = copie.copy(extra_answers=generate_copier_answers())

    assert result.exit_code == 0
    assert result.exception is None
    assert result.project_dir.is_dir()

    assert result.project_dir.joinpath('.editorconfig').exists()


def test_template_licenses(copie: Copie):
    for license_id, license_spec in LICENSE_SPEC.items():
        answers = generate_copier_answers()
        answers['copyright_license'] = license_id

        result = copie.copy(extra_answers=answers)

        assert result.exit_code == 0
        assert result.exception is None
        assert result.project_dir.is_dir()

        license_text = result.project_dir.joinpath(license_spec['filename']).read_text(encoding='utf-8')
        assert license_spec['stub'] in license_text

        if license_spec['with_holder']:
            assert f'{answers["copyright_holder_name"]} <{answers["copyright_holder_email"]}>' in license_text
            assert answers['copyright_year'] in license_text

        assert result.project_dir.joinpath(get_license_file(license_id)).exists()

        readme = result.project_dir.joinpath('README.md').read_text()

        assert answers['project_name'] in readme
        assert answers['project_description'] in readme

        assert license_spec['stub'] in readme

        if license_id == 'Unlicense':
            assert 'This is free and unencumbered software released into the public domain' in readme
        else:
            assert f'Copyright (C) {answers["copyright_year"]} {answers["copyright_holder_name"]} <{answers["copyright_holder_email"]}>' in readme
            assert f'see [{license_spec["filename"]}](./{license_spec["filename"]}).' in readme
