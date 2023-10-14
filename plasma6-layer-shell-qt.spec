%define stable %([ "`echo %{version} |cut -d. -f3`" -ge 80 ] && echo -n un; echo -n stable)
%define major 6
%define git 20231014

Name:		plasma6-layer-shell-qt
Version:	5.240.0
Release:	%{?git:0.%{git}.}1
Summary:	Qt component to allow applications to make use of the Wayland wl-layer-shell protocol
Group:		System/Libraries
License:	GPLv2
URL:		https://kde.org/
%if 0%{?git:1}
Source0:	https://invent.kde.org/plasma/layer-shell-qt/-/archive/master/layer-shell-qt-master.tar.bz2#/layer-shell-qt-%{git}.tar.bz2
%else
Source0:	http://download.kde.org/%{stable}/plasma/%{version}/%{name}-%{version}.tar.xz
%endif
# Bump soname to avoid a nasty conflict between Plasma 5 and 6 both
# trying to own libLayerShellQtInterface.so.5
Patch0:		layer-shell-qt-bump-soname.patch
BuildRequires:	ninja
BuildRequires:	cmake(ECM)
BuildRequires:	cmake(Qt6)
BuildRequires:	cmake(Qt6Core)
BuildRequires:	cmake(Qt6DBus)
BuildRequires:	cmake(Qt6Gui)
BuildRequires:	cmake(Qt6WaylandClient)
BuildRequires:	cmake(Qt6Qml)
BuildRequires:	cmake(Qt6Quick)
BuildRequires:	cmake(WaylandProtocols)
BuildRequires:	cmake(PlasmaWaylandProtocols)
BuildRequires:	pkgconfig(wayland-client)
BuildRequires:	pkgconfig(wayland-protocols)
BuildRequires:	pkgconfig(xkbcommon)
# Just to prevent pulling in Plasma 5
BuildRequires:	plasma6-xdg-desktop-portal-kde

%description
Qt component to allow applications to make use of the Wayland wl-layer-shell protocol

%files
%dir %{_qtdir}/plugins/wayland-shell-integration
%{_qtdir}/plugins/wayland-shell-integration/liblayer-shell.so
# No need to split this into a package of its own, the library is useless
# without the Qt plugin
%{_libdir}/libLayerShellQtInterface.so.*

#------------------------------------------------------------------------------
%define devname %mklibname LayerShellQtInterface -d

%package -n %{devname}
Summary:	Devel stuff for %{name}
Group:		Development/KDE and Qt
Requires:	%{name} = %{EVRD}

%description -n %{devname}
Qt component to allow applications to make use of the Wayland wl-layer-shell protocol

%files -n %{devname}
%{_libdir}/libLayerShellQtInterface.so
%{_includedir}/LayerShellQt
%{_libdir}/cmake/LayerShellQt

#------------------------------------------------------------------------------

%prep
%autosetup -p1 -n layer-shell-qt-%{?git:master}%{!?git:%{version}}
%cmake \
	-DBUILD_QCH:BOOL=ON \
	-DBUILD_WITH_QT6:BOOL=ON \
	-DKDE_INSTALL_USE_QT_SYS_PATHS:BOOL=ON \
	-G Ninja

%build
%ninja_build -C build

%install
%ninja_install -C build
