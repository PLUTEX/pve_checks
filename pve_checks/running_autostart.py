from proxmoxer import ProxmoxAPI

from . import call_function
from .nagios import ResultCode, NagiosResult


def check(pve: ProxmoxAPI = None):
    if not pve:
        # we need to make the argument itself optional for argh
        raise RuntimeError('pve parameter missing')

    for node in pve.nodes.get():
        for vm in pve.nodes(node['node']).qemu.get():
            vm_config = pve.nodes(node['node']).qemu(vm['vmid']).config.get()
            onboot = vm_config.get('onboot', 0)
            if (vm['status'] == 'running') ^ (onboot == 1):
                yield NagiosResult(
                    code=ResultCode.WARNING,
                    summary='',  # unused at this stage
                    details='{} on {} is {} but autostart={}'.format(
                        node['node'],
                        vm['name'],
                        vm['status'],
                        onboot,
                    )
                )


def main():
    call_function(check)


if __name__ == '__main__':
    main()