# -*- coding: utf-8 -*-
from os import listdir, path


def install(template_vars, local_tpl_dir):
    c.sudo("pip2 install circus")

    for filename in listdir(local_tpl_dir):
        name, ext = path.splitext(filename)
        if name == "circus":
            full_path = path.join(local_tpl_dir, filename)
            if ext == ".conf":
                upload_template_fmt(
                    c,
                    full_path,
                    "/etc/init/circus.conf",
                    context=template_vars,
                    use_sudo=True,
                )
            elif ext == ".ini":
                c.run(
                    "mkdir -p {remote_home}/conf".format(
                        remote_home=template_vars["HOME"]
                    )
                )
                upload_template_fmt(
                    c,
                    full_path,
                    "{remote_home}/conf/circus.ini".format(
                        remote_home=template_vars["HOME"]
                    ),
                    context=template_vars,
                )

    c.sudo("initctl reload-configuration")
    """ dbus-send --system --print-reply --dest=com.ubuntu.Upstart
                  /com/ubuntu/Upstart/jobs/circus/_ org.freedesktop.DBus.Properties.GetAll string:''
                  method return sender=:1.0 -> dest=:1.726 reply_serial=2 """
    if c.sudo("service circus status").endswith("stop/waiting"):
        c.sudo("service circus start")

    # TODO: Write this to a logfile with a timestamp instead
    c.run("mkdir -p $HOME/.setup")
    c.run("touch $HOME/.setup/circus")
