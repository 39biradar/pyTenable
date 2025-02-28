import pytest
from ..checker import check


def test_groups_constructor_name_typeerror(sc):
    with pytest.raises(TypeError):
        sc.groups._constructor(name=1)


def test_groups_constructor_description_typeerror(sc):
    with pytest.raises(TypeError):
        sc.groups._constructor(description=1)


def test_groups_constructor_list_mapping_typeerror(sc):
    items = ['viewable', 'repos', 'lce_ids', 'asset_lists', 'scan_policies',
             'query_ids', 'scan_creds', 'dashboards', 'report_cards', 'audit_files']
    for i in items:
        with pytest.raises(TypeError):
            sc.groups._constructor(**{i: 1})


def test_groups_constructor_list_item_mapping_typeerror(sc):
    items = ['viewable', 'repos', 'lce_ids', 'asset_lists', 'scan_policies',
             'query_ids', 'scan_creds', 'dashboards', 'report_cards', 'audit_files']
    for item in items:
        with pytest.raises(TypeError):
            sc.groups._constructor(**{item: ['one']})


def test_groups_constructor_success(sc):
    group = sc.groups._constructor(
        name='Example',
        description='Stuff',
        viewable=[1, 2, 3],
        repos=[1],
        lce_ids=[1],
        asset_lists=[1, 2],
        scan_policies=[1],
        query_ids=[1],
        scan_creds=[1, 2, 3],
        dashboards=[1, 2],
        report_cards=[1],
        audit_files=[1, 2]
    )
    assert isinstance(group, dict)
    assert group == {
        'name': 'Example',
        'description': 'Stuff',
        'definingAssets': [{'id': 1}, {'id': 2}, {'id': 3}],
        'repositories': [{'id': 1}],
        'lces': [{'id': 1}],
        'assets': [{'id': 1}, {'id': 2}],
        'policies': [{'id': 1}],
        'queries': [{'id': 1}],
        'credentials': [{'id': 1}, {'id': 2}, {'id': 3}],
        'dashboardTabs': [{'id': 1}, {'id': 2}],
        'arcs': [{'id': 1}],
        'auditFiles': [{'id': 1}, {'id': 2}]
    }


@pytest.mark.vcr()
def test_groups_create_success(sc, group):
    assert isinstance(group, dict)
    check(group, 'id', str)
    check(group, 'name', str)
    check(group, 'description', str)
    check(group, 'createdTime', str)
    check(group, 'modifiedTime', str)
    check(group, 'userCount', int)
    key_list = ['definingAssets', 'lces', 'repositories', 'assets', 'policies',
               'queries', 'credentials', 'dashboardTabs', 'arcs', 'auditFiles']
    for key in key_list:
        check(group, key, list)
        for group in group[key]:
            check(group, 'id', str)
            check(group, 'name', str)
            check(group, 'description', str)
            if key == 'lces':
                check(group, 'version', str)
            if key == 'repositories':
                check(group, 'lastVulnUpdate', str)
                check(group, 'type', str)
                check(group, 'dataFormat', str)


@pytest.mark.vcr()
def test_groups_edit_success(sc, group):
    group = sc.groups.edit(int(group['id']), name='new name')
    assert isinstance(group, dict)
    check(group, 'id', str)
    check(group, 'name', str)
    check(group, 'description', str)
    check(group, 'createdTime', str)
    check(group, 'modifiedTime', str)
    check(group, 'userCount', int)
    key_list = ['definingAssets', 'lces', 'repositories', 'assets', 'policies',
               'queries', 'credentials', 'dashboardTabs', 'arcs', 'auditFiles']
    for key in key_list:
        check(group, key, list)
        for a_group in group[key]:
            check(a_group, 'id', str)
            check(a_group, 'name', str)
            check(a_group, 'description', str)
            if key == 'lces':
                check(a_group, 'version', str)
            if key == 'repositories':
                check(a_group, 'lastVulnUpdate', str)
                check(a_group, 'type', str)
                check(a_group, 'dataFormat', str)


@pytest.mark.vcr()
def test_groups_details_success_for_fields(sc, group):
    group = sc.groups.details(int(group['id']), fields=['id', 'name', 'description'])
    assert isinstance(group, dict)
    check(group, 'id', str)
    check(group, 'name', str)
    check(group, 'description', str)


@pytest.mark.vcr()
def test_groups_list_success_for_fields(sc, group):
    groups = sc.groups.list(fields=['id', 'name', 'description'])
    assert isinstance(groups, list)
    for group in groups:
        check(group, 'id', str)
        check(group, 'name', str)
        check(group, 'description', str)


@pytest.mark.vcr()
def test_groups_details_success(sc, group):
    g = sc.groups.details(int(group['id']))
    assert isinstance(g, dict)
    check(g, 'id', str)
    check(g, 'name', str)
    check(g, 'description', str)
    check(g, 'createdTime', str)
    check(g, 'modifiedTime', str)
    check(g, 'userCount', int)
    keylist = ['definingAssets', 'lces', 'repositories', 'assets', 'policies',
               'queries', 'credentials', 'dashboardTabs', 'arcs', 'auditFiles']
    for i in keylist:
        check(g, i, list)
        for j in g[i]:
            check(j, 'id', str)
            check(j, 'name', str)
            check(j, 'description', str)
            if i == 'lces':
                check(j, 'version', str)
            if i == 'repositories':
                check(j, 'lastVulnUpdate', str)
                check(j, 'type', str)
                check(j, 'dataFormat', str)


@pytest.mark.vcr()
def test_groups_delete_success(sc, group):
    sc.groups.delete(int(group['id']))
