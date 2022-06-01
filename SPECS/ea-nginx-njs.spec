Name:           ea-nginx-njs
Version:        0.7.4
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
* Thu May 26 2022 Cory McIntire <cory@cpanel.net> - 0.7.4-1
- EA-10737: Update ea-nginx-njs from v0.7.3 to v0.7.4

* Mon Apr 18 2022 Cory McIntire <cory@cpanel.net> - 0.7.3-1
- EA-10645: Update ea-nginx-njs from v0.7.2 to v0.7.3

* Thu Feb 24 2022 Daniel Muey <dan@cpanel.net> - 0.7.2-1
- ZC-9697: Initial version
