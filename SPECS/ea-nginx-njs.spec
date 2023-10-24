Name:           ea-nginx-njs
Version:        0.8.2
# Doing release_prefix this way for Release allows for OBS-proof versioning, See EA-4552 for more details
%define release_prefix 1
Release:        %{release_prefix}%{?dist}.cpanel
Summary:        njs scripting language for ea-nginx
License:        2-clause BSD-like license
Group:          System Environment/Libraries
URL:            http://www.cpanel.net
Vendor:         cPanel, Inc.
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot

BuildRequires:  ea-nginx-ngxdev
BuildRequires:  libxml2
BuildRequires:  libxml2-devel
BuildRequires:  libxslt-devel
Requires:       ea-nginx

Source0:        %{version}.tar.gz
Source1:        ngx_njs_module.conf

%description
njs is a subset of the JavaScript language that allows extending nginx
functionality. njs is created in compliance with ECMAScript 5.1 (strict mode)
with some ECMAScript 6 and later extensions. The compliance is still evolving.
More information on how to use it can be found at https://nginx.org/en/docs/njs/
This package covers the 'Download and install' portions of that document as
well as loading the modules. All you need to do is add the njs directives
into your custom configurations.

%prep
%setup -q -n njs-%{version}

%build

# You will be in ./nginx-build after this source()
#    so that configure and make etc can happen.
# We probably want to popd back when we are done in there
. /opt/cpanel/ea-nginx-ngxdev/set_NGINX_CONFIGURE_array.sh
./configure "${NGINX_CONFIGURE[@]}" --add-dynamic-module=../nginx/
make %{?_smp_mflags}
popd

%install
mkdir -p %{buildroot}/etc/nginx/conf.d/modules
install %{SOURCE1} %{buildroot}/etc/nginx/conf.d/modules/ngx_njs_module.conf

mkdir -p %{buildroot}%{_libdir}/nginx/modules
install ./nginx-build/objs/ngx_stream_js_module.so %{buildroot}%{_libdir}/nginx/modules/ngx_stream_js_module.so
install ./nginx-build/objs/ngx_http_js_module.so %{buildroot}%{_libdir}/nginx/modules/ngx_http_js_module.so

%clean
rm -rf %{buildroot}

%files
%defattr(0644,root,root,0755)
/etc/nginx/conf.d/modules/ngx_njs_module.conf
%attr(0755,root,root) %{_libdir}/nginx/modules/ngx_http_js_module.so
%attr(0755,root,root) %{_libdir}/nginx/modules/ngx_stream_js_module.so

%changelog
* Tue Oct 24 2023 Cory McIntire <cory@cpanel.net> - 0.8.2-1
- EA-11761: Update ea-nginx-njs from v0.8.1 to v0.8.2

* Fri Sep 15 2023 Cory McIntire <cory@cpanel.net> - 0.8.1-1
- EA-11685: Update ea-nginx-njs from v0.8.0 to v0.8.1

* Thu Aug 24 2023 Cory McIntire <cory@cpanel.net> - 0.8.0-2
- EA-11631: Build against ea-nginx version v1.25.2

* Fri Jul 07 2023 Cory McIntire <cory@cpanel.net> - 0.8.0-1
- EA-11537: Update ea-nginx-njs from v0.7.12 to v0.8.0

* Thu Jun 15 2023 Cory McIntire <cory@cpanel.net> - 0.7.12-2
- EA-11496: Build against ea-nginx version v1.25.1

* Wed Apr 12 2023 Cory McIntire <cory@cpanel.net> - 0.7.12-1
- EA-11351: Update ea-nginx-njs from v0.7.11 to v0.7.12

* Fri Mar 10 2023 Cory McIntire <cory@cpanel.net> - 0.7.11-1
- EA-11297: Update ea-nginx-njs from v0.7.10 to v0.7.11

* Fri Feb 10 2023 Cory McIntire <cory@cpanel.net> - 0.7.10-1
- EA-11224: Update ea-nginx-njs from v0.7.9 to v0.7.10

* Thu Nov 17 2022 Cory McIntire <cory@cpanel.net> - 0.7.9-1
- EA-11059: Update ea-nginx-njs from v0.7.8 to v0.7.9

* Thu Oct 27 2022 Cory McIntire <cory@cpanel.net> - 0.7.8-1
- EA-11017: Update ea-nginx-njs from v0.7.7 to v0.7.8

* Tue Aug 30 2022 Cory McIntire <cory@cpanel.net> - 0.7.7-1
- EA-10904: Update ea-nginx-njs from v0.7.6 to v0.7.7

* Tue Jul 19 2022 Cory McIntire <cory@cpanel.net> - 0.7.6-1
- EA-10836: Update ea-nginx-njs from v0.7.5 to v0.7.6

* Tue Jun 21 2022 Cory McIntire <cory@cpanel.net> - 0.7.5-1
- EA-10772: Update ea-nginx-njs from v0.7.4 to v0.7.5

* Thu May 26 2022 Cory McIntire <cory@cpanel.net> - 0.7.4-1
- EA-10737: Update ea-nginx-njs from v0.7.3 to v0.7.4

* Mon Apr 18 2022 Cory McIntire <cory@cpanel.net> - 0.7.3-1
- EA-10645: Update ea-nginx-njs from v0.7.2 to v0.7.3

* Thu Feb 24 2022 Daniel Muey <dan@cpanel.net> - 0.7.2-1
- ZC-9697: Initial version
