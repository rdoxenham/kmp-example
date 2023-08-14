#
# spec file for KMP package at25
#
# Copyright (c) 2023 SUSE LINUX GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via http://bugs.opensuse.org/
#


# norootforbuild

Name:           	at25
Version:                1.0
Release:                0
Summary:                Kernel Module Package for at25 module
License:                GPL-2.0
Group:          	System/Kernel
URL:                    https://www.suse.com
Source0:                %{name}-%{version}.tar.gz
# Required to sign modules:  Include certificate named “signing_key.x509”
# Build structure should also include a private key named “signing_key.priv”
# Private key should not be listed as a source file
Source1:        signing_key.x509
ExclusiveArch:	aarch64
BuildRequires:  %kernel_module_package_buildreqs
BuildRequires:  bash-sh
BuildRequires:  systemd
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

# Required to sign modules:  The -c option tells the macro to generate a
# suse-hello-ueficert subpackage that enrolls the certificate
%suse_kernel_module_package -c %_sourcedir/signing_key.x509 -b

%description
This package contains the at25.ko module.

%prep
%setup
# Required to sign modules:  Copy the signing key to the build area
cp %_sourcedir/signing_key.* .
set -- *
mkdir source
mv "$@" source/
mkdir obj

%build
for flavor in %flavors_to_build; do
       rm -rf obj/$flavor
       cp -r source obj/$flavor
       make -C %{kernel_source $flavor} modules M=$PWD/obj/$flavor
done

%install
export INSTALL_MOD_PATH=$RPM_BUILD_ROOT
export INSTALL_MOD_DIR=updates
for flavor in %flavors_to_build; do
       make -C %{kernel_source $flavor} modules_install M=$PWD/obj/$flavor
       # Required to sign modules:  Invoke kernel-sign-file to sign each module
       for x in $(find $INSTALL_MOD_PATH/lib/modules/*-$flavor/ -name '*.ko'); do
               /usr/lib/rpm/pesign/kernel-sign-file -i pkcs7 sha256 $PWD/obj/$flavor/signing_key.priv $PWD/obj/$flavor/signing_key.x509 $x
       done
done

%files

%changelog
* Thu Aug 10 2023 Rhys Oxenham <rhys.oxenham@suse.com> - 1.0
- Base spec file to be used as a KMP example for adding EEPROM at25 support.
