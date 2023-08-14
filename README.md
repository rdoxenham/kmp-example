SUSE Kernel Module Package (KMP) Example
========================================

This repo will enable you to create a kernel module package (KMP) for SLES15-SP4 (and SLE Micro). The example builds the in-tree at25 kernel module, but is currently not set in the kernel config, so isn't built by default.

Steps to produce your own module based on this repo:

1. Create the necessary kernel module signing keys (see signing_key_setup.txt for an example).

2. You'll need the kernel module Makefile, the source, and any headers required.

3. Test with `make -C /lib/modules/\`uname -r\`/build M=\`pwd\` modules`

4. Clean up with `make -C /lib/modules/\`uname -r\`/build M=\`pwd\` clean`

5. Create a tarball of your source directory, and create a spec file (see at25.spec as an example).

6. Build the module with `build --dist /usr/lib/build/configs/sle15.4.conf` this can be installed on SLE, or from https://github.com/openSUSE/obs-build

7. You'll find the RPM's at: /var/tmp/build-root/home/abuild/rpmbuild/RPMS/<arch>/

8. Install on SLES/SLE Micro (via transactional-update). Note that if your module is required pre pivot root, make sure your initrd is rebuilt, and if necessary, add it via /etc/dracut.conf.d (`add_driver+=" <your module> "` - the spaces are important!)

Further information: https://documentation.suse.com/sbp/all/html/SBP-KMP-Manual-SLE12SP2/index.html
