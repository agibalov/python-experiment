import everett
from everett.manager import ConfigManager, ConfigOSEnv, ConfigDictEnv
from everett.ext.yamlfile import ConfigYamlEnv
import pytest


def test_dummy():
    config = ConfigManager([
        ConfigYamlEnv('my.yaml'),
        ConfigOSEnv(),
        ConfigDictEnv({
            'COMESFROMDICT': 'comes from dict'
        })
    ])
    assert config('comesfromyaml') == 'comes from yaml'
    assert config('THIS_COMES_FROM_YAML') == 'too'
    assert config.with_namespace('this').with_namespace('comes').with_namespace('from')('yaml') == 'too'
    assert config('USER') == 'aagibalov'
    assert config('comesfromdict') == 'comes from dict'

    try:
        config('SomeSecret')
        pytest.fail()
    except everett.ConfigurationError:
        pass

    assert config('SomeSecret', default='SomeDefault') == 'SomeDefault'
