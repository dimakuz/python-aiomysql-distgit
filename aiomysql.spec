%global pypi_name aiomysql

Name:           python-%{pypi_name}
Version:        0.0.20
Release:        1%{?dist}
Summary:        aiomysql is a "driver" for accessing a MySQL database from the asyncio (PEP-3156/tulip) framework.

License:        MIT
URL:            https://github.com/aio-libs/aiomysql
Source0:        %{url}/archive/%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch

%global _description \
FIXME

%description %{_description}

%package -n     python%{python3_pkgversion}-%{pypi_name}
Summary:        %{summary}
%{?python_provide:%python_provide python%{python3_pkgversion}-%{pypi_name}}
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-setuptools

%description -n python%{python3_pkgversion}-%{pypi_name} %{_description}

Python 3 version.

%prep
%autosetup -n %{pypi_name}-%{version} -p1

%build
%py3_build

%install
%py3_install

%check

%files -n python%{python3_pkgversion}-%{pypi_name}
%license LICENSE
%doc README.rst CHANGES.txt
%{python3_sitelib}/aiomysql-*.dist-info/
%{python3_sitelib}/%{pypi_name}/

%changelog
