from os import path

from offregister_fab_utils.apt import apt_depends


def install(local_conf_path, service_cmd="restart", name=None, template_vars=None):
    apt_depends(c, "nginx-full")

    remote_conf_name = name or path.basename(local_conf_path).partition(path.extsep)[0]
    remote_path = "/etc/nginx/sites-available/{remote_conf_name}".format(
        remote_conf_name=remote_conf_name
    )

    c.sudo(
        "rm -f /etc/nginx/sites-enabled/{remote_conf_name}".format(
            remote_conf_name=remote_conf_name
        )
    )
    c.sudo("rm -f /etc/nginx/sites-enabled/default")
    c.sudo("rm -f /etc/nginx/sites-available/default")
    if template_vars:
        upload_template_fmt(
            c, local_conf_path, remote_path, context=template_vars, use_sudo=True
        )
    else:
        c.put(local_conf_path, remote=remote_path, use_sudo=True)
    # c.put(default_conf_path, '/etc/nginx/sites-enabled/default', use_sudo=True)
    c.sudo(
        "ln -s /etc/nginx/sites-available/{remote_conf_name} /etc/nginx/sites-enabled/{remote_conf_name}".format(
            remote_conf_name=remote_conf_name
        )
    )
    c.sudo("service nginx {service_cmd}".format(service_cmd=service_cmd))
