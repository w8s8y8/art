import os
import xlrd
import xml.dom.minidom
import time


def delete_file_folder(src):
    if os.path.isfile(src):
        try:
            os.remove(src)
        except:
            pass
    elif os.path.isdir(src):
        for item in os.listdir(src):
            delete_file_folder(os.path.join(src, item))
        try:
            os.rmdir(src)
        except:
            pass


def scl_prepare_dir(dir_name):
    delete_file_folder(dir_name)
    os.mkdir(dir_name)


def scl_read_excel():
    for file_name in os.listdir(os.getcwd()):
        if os.path.isfile(file_name) and os.path.splitext(file_name)[1] in ('.xls', '.xlsx'):
            table = xlrd.open_workbook(file_name).sheets()[0]
            xls_ied = {}
            for row in range(1, table.nrows):
                ied_name = table.cell(row, 2).value
                if ied_name in xls_ied:
                    xls_ied[ied_name].append(table.cell(row, 1).value)
                else:
                    xls_ied[ied_name] = [table.cell(row, 1).value]
            return xls_ied


def scl_path(scl, path):
    for single_path in path:
        if scl is None:
            return None
        for element in scl.getElementsByTagName(single_path[0]):
            match = True
            if len(single_path) > 1:
                for attribute_name, attribute_value in single_path[1].items():
                    if attribute_value != element.getAttribute(attribute_name):
                        match = False
                        break
            scl = element if match else None
            if match:
                break
    return scl


def scl_yx(ied_name, file_name, yx_list):
    doc = xml.dom.minidom.parse(file_name)

    ied_hash = {}

    # 遍历所有的SubNetwork节点
    for sn in doc.getElementsByTagName('SubNetwork'):
        # 在SubNetwork节点下查找有该IED字段且有IP字段
        for ap in sn.childNodes:
            if ap.nodeType == ap.ELEMENT_NODE and ap.getAttribute('iedName') == ied_name:
                if ap.getAttribute('apName') in ('G1', 'M1'):
                    continue
                for address in ap.childNodes:
                    if address.nodeType == address.ELEMENT_NODE and address.tagName == 'Address':
                        for p in address.childNodes:
                            if p.nodeType == p.ELEMENT_NODE and p.tagName == 'P' and p.getAttribute('type') == 'IP':
                                    if p.firstChild:
                                        ied_hash['IP'] = p.firstChild.nodeValue
                                        break
                    if 'IP' in ied_hash:
                        break
            if 'IP' in ied_hash:
                ied_hash['AP'] = ap.getAttribute('apName')
                break
        if 'AP' in ied_hash:
            ied_hash['SubNetworkName'] = sn.getAttribute('name')
            ied_hash['SubNetworkType'] = sn.getAttribute('type')
            break

    print('----', ied_name, ied_hash['IP'], ied_hash['AP'], '----')

    ied_node = scl_path(doc, [['IED', {'name': ied_name}], ['AccessPoint', {'name': ied_hash['AP']}], ['Server']])
    templates = scl_path(doc, [['DataTypeTemplates']])

    yx_array = []

    for yx_path in yx_list:
        yx = {'IED': ied_name, 'Path': yx_path}
        ld_name, temp = yx_path.split('/')
        ln_name, do_name = temp.split('.')
        ld = scl_path(ied_node, [['LDevice', {'inst': ld_name}]])  # 查找LDevice
        lln0 = scl_path(ld, [['LN0', {'lnClass': 'LLN0'}]])  # 查找LLN0
        for ln in ld.getElementsByTagName('LN'):  # 查找LN
            if ln.getAttribute('prefix') + ln.getAttribute('lnClass') + ln.getAttribute('inst') == ln_name:
                if scl_path(ln, [['DOI', {'name': do_name}]]) is not None:  # 查找DOI
                    yx['name'] = do_name
                    yx['prefix'] = ln.getAttribute('prefix')
                    yx['lnClass'] = ln.getAttribute('lnClass')
                    yx['lnInst'] = ln.getAttribute('inst')
                    yx['lnType'] = ln.getAttribute('lnType')
                    yx['ldInst'] = ld_name

                    for ds in lln0.getElementsByTagName('DataSet'):  # 查找DataSet
                        # 查找DataSet下的FCDA
                        if scl_path(ds, [['FCDA', {'doName': yx['name'],  'lnInst': yx['lnInst'],
                                                   'prefix': yx['prefix'], 'ldInst': yx['ldInst']}]])\
                                is not None:
                            yx['DataSet'] = ds.getAttribute('name')
                            # 查找Report
                            report = scl_path(lln0, [['ReportControl', {'datSet': ds.getAttribute('name')}]])
                            if report is not None:
                                yx['Report'] = report.getAttribute('name')
                                yx['ReportType'] = 'BR' if report.getAttribute('buffered') == 'true' else 'RP'
                                break

                        if 'Report' in yx:
                            do = scl_path(templates, [['LNodeType', {'id': yx['lnType']}],
                                                      ['DO', {'name': yx['name']}]])
                            if do is not None:
                                yx['Type'] = do.getAttribute('type')  # 查找DO的类型
                            break
                break
        # print(yx)
        yx_array.append(yx)

    return {'IED': ied_name, 'YX': yx_array, 'IP': ied_hash['IP'], 'AP': ied_hash['AP'],
            'SubNetworkName': ied_hash['SubNetworkName'], 'SubNetworkType': ied_hash['SubNetworkType']}


def scl_check_yx(ied_array):
    error_string_array = []
    for ied_hash in ied_array:
        for yx in ied_hash['YX']:
            if 'ldInst' not in yx:
                error_string_array.append("\"" + yx['IED'] + '$' + yx['Path'] + "\" Can't Find LogicNode")
            elif 'DataSet' not in yx:
                error_string_array.append("\"" + yx['IED'] + '$' + yx['Path'] + "\" Can't Find DataSet")
            elif 'Report' not in yx:
                error_string_array.append("\"" + yx['IED'] + '$' + yx['Path'] + "\" Can't Find Report")

    error_count = len(error_string_array)
    print('\n================ There is', error_count, 'Error ================')
    print('\n'.join(error_string_array))

    if error_count == 0:
        for ied_hash in ied_array:
            ds = []
            rpcb = []
            for yx in ied_hash['YX']:
                r = yx['ldInst'] + '/LLN0$' + yx['ReportType'] + '$' + yx['Report']
                if r not in rpcb:
                    rpcb.append(r)
                d = yx['DataSet']
                if d not in ds:
                    ds.append(d)
            print(ied_hash['IED'], '\t', ied_hash['IP'], '\t', ied_hash['AP'],
                  '\t', ';'.join(ds), '\t', ';'.join(rpcb))

    return error_count


def scl_remove_node(node):
    parent = node.parentNode
    previous = node.previousSibling
    if previous.nodeType == previous.TEXT_NODE:
        parent.removeChild(previous)
    parent.removeChild(node)


def scl_remove_node_with_parent(node, parent):
    previous = node.previousSibling
    if previous.nodeType == previous.TEXT_NODE:
        parent.removeChild(previous)
    parent.removeChild(node)


def scl_remove_node_except(node, tag_name, path):
    node = scl_path(node, path)
    if node is not None:
        parent = node.parentNode
        if parent is not None:
            for element in parent.getElementsByTagName(tag_name):
                if element != node:
                    scl_remove_node_with_parent(element, parent)


def scl_remove_node_except_hash(node, tag_name, attribute_name, keep_hash):
    elements = node.getElementsByTagName(tag_name)
    parent_element = elements[0].parentNode
    for element in elements:
        if keep_hash:
            need_remove = True
            for attribute in keep_hash.keys():
                if element.getAttribute(attribute_name) == attribute:
                    del keep_hash[attribute]
                    need_remove = False
                    break
            if need_remove:
                scl_remove_node_with_parent(element, parent_element)
        else:
            scl_remove_node_with_parent(element, parent_element)


def scl_remove_ln(ld_path, ln0_path):
    fcda = dict()
    for da in ln0_path.getElementsByTagName('FCDA'):
        fcda[da] = da

    for ln in ld_path.getElementsByTagName('LN'):
        if ln.getAttribute('lnClass') != 'LPHD':
            if fcda:
                need_remove = True
                for da in fcda:
                    if da.getAttribute('prefix') == ln.getAttribute('prefix') and \
                                    da.getAttribute('lnClass') == ln.getAttribute('lnClass') and \
                                    da.getAttribute('lnInst') == ln.getAttribute('inst'):
                            del fcda[da]
                            need_remove = False
                            break
                if need_remove:
                    scl_remove_node_with_parent(ln, ld_path)
            else:
                scl_remove_node_with_parent(ln, ld_path)


def scl_remove_node_all(scl, tag_name):
    for node in scl.getElementsByTagName(tag_name):
        scl_remove_node(node)


def scl_ld_and_ds_statistic(ied_hash):
    ld_and_ds_statistic = dict()

    ld_and_ds_statistic['List'] = dict()
    ld_and_ds_statistic['Value'] = dict()

    ld_and_ds_list = ld_and_ds_statistic['List']
    ld_and_ds_value = ld_and_ds_statistic['Value']

    ld_list = []
    for yx in ied_hash['YX']:
        if yx['ldInst'] not in ld_list:
            ld_list.append(yx['ldInst'])
            ld_and_ds_value[yx['ldInst']] = [{}, {}, {}]

    for yx in ied_hash['YX']:
        value = ld_and_ds_value[yx['ldInst']]
        value[0][yx['Report']] = 1
        value[1][yx['DataSet']] = 1
        value[2][yx['Path']] = 1

    for ied_name in ld_and_ds_value.keys():
        ld_and_ds_list[ied_name] = 1

    return ld_and_ds_statistic


def scl_ln_type_statistic(scl):
    ied_node = scl_path(scl, [['IED']])
    ln_types = dict()
    for ln in ied_node.getElementsByTagName('LN'):
        ln_types[ln.getAttribute('lnType')] = 1
    for ln0 in ied_node.getElementsByTagName('LN0'):
        ln_types[ln0.getAttribute('lnType')] = 1
    return ln_types


def scl_da_type_statistic(scl):
    templates = scl_path(scl, 'DataTypeTemplates')
    da_types = dict()
    for da in templates.getElementsByTagName('DA'):
        if da.getAttribute('bType') == 'Struct':
            da_types[da.getAttribute('type')] = 1
    for bda in templates.getElementsByTagName('BDA'):
        if bda.getAttribute('bType') == 'Struct':
            da_types[bda.getAttribute('type')] = 1
    return da_types


def scl_do_type_statistic(scl, tag_name, attribute_name):
    do_types = dict()
    for do in scl.getElementsByTagName(tag_name):
        do_types[do.getAttribute(attribute_name)] = 1
    return do_types


def scl_strip(iedhash, cid_dir_name, cfg_dir_name):
    doc = xml.dom.minidom.parse(cid_dir_name + iedhash['IED'] + '.cid')
    
    header = doc.getElementsByTagName('Header')[0]
    header.setAttribute('toolID', '全自动校验与裁剪CID文件工具')
    header.setAttribute('version', '9.9')
    header.setAttribute('revision', 'T')
    header.setAttribute('when', time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    header.setAttribute('who', '无面者')

    elements = doc.getElementsByTagName('Hitem')
    if len(elements) > 1:
        remain_item = elements.pop()
        history_node = elements[0].parentNode
        for element in elements:
            scl_remove_node_with_parent(element, history_node)
        next_value = remain_item.nextSibling.nodeValue
        history_node.removeChild(remain_item.nextSibling)
        hitem_node = doc.createElement('Hitem')
        hitem_node.setAttribute('version', '8')
        hitem_node.setAttribute('revision', '8')
        hitem_node.setAttribute('when', time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        hitem_node.setAttribute('why', '五防IEC61850规约转换器')
        hitem_node.setAttribute('what', 'CID文件自动裁剪')
        hitem_node.setAttribute('who', '韦树远')
        history_node.appendChild(doc.createTextNode(remain_item.previousSibling.nodeValue))
        history_node.appendChild(hitem_node)
        history_node.appendChild(doc.createTextNode(next_value))

    scl_remove_node_except(doc, 'SubNetwork',
                           [['SubNetwork', {'name': iedhash['SubNetworkName'], 'type': iedhash['SubNetworkType']}]])
    scl_remove_node_except(doc, 'IED', [['IED', {'name': iedhash['IED']}]])
    scl_remove_node_except(doc, 'AccessPoint', [['AccessPoint', {'name': iedhash['AP']}]])

    ld_and_ds_statistic = scl_ld_and_ds_statistic(iedhash)

    scl_remove_node_except_hash(scl_path(doc, [['AccessPoint', {'name': iedhash['AP']}]]), 'LDevice', 'inst',
                                ld_and_ds_statistic['List'].copy())

    for ld_name in ld_and_ds_statistic['List'].keys():
        ld_path = scl_path(doc, [['LDevice', {'inst': ld_name}]])
        ln0_path = scl_path(ld_path, [['LN0', {'lnClass': 'LLN0'}]])

        if ln0_path is not None:
            scl_remove_node_except_hash(ln0_path, 'ReportControl', 'name', ld_and_ds_statistic['Value'][ld_name][0])
            scl_remove_node_except_hash(ln0_path, 'DataSet', 'name', ld_and_ds_statistic['Value'][ld_name][1])

            scl_remove_ln(ld_path, ln0_path)

    scl_remove_node_except_hash(doc, 'LNodeType', 'id', scl_ln_type_statistic(doc))

    scl_remove_node_except_hash(doc, 'DOType', 'id', scl_do_type_statistic(doc, 'DO', 'type'))

    scl_remove_node_except_hash(doc, 'DAType', 'id', scl_da_type_statistic(doc))

    scl_remove_node_all(doc, 'Private')
    scl_remove_node_all(doc, 'ExtRef')
    scl_remove_node_all(doc, 'GSEControl')
    scl_remove_node_all(doc, 'GSE')

    for element in doc.getElementsByTagName('DAI'):
        if not element.hasChildNodes():
            scl_remove_node(element)
        elif element.hasAttribute('sAddr'):
            element.removeAttribute('sAddr')

    doc.writexml(open(cfg_dir_name + iedhash['IED'] + '.cid', 'w', encoding='utf-8'))


if __name__ == '__main__':
    print('---==== SCL PointCheck & Strip ====---\n')

    cid_dir = 'cid/'
    cfg_dir = 'cfg/'

    scl_prepare_dir(cfg_dir)
    
    xls = scl_read_excel()
    ieds = []
    for cid_name in xls.keys():
        ieds.append(scl_yx(cid_name, cid_dir + cid_name + '.cid', xls[cid_name]))

    if scl_check_yx(ieds) == 0:
        for ied in ieds:
            scl_strip(ied, cid_dir, cfg_dir)
