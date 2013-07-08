# 
# Do NOT Edit the Auto-generated Part!
# Generated by: spectacle version 0.22
# 
# >> macros
# << macros

Name:       mthemedaemon
Summary:    Shared theme resource loader
Version:    1.0.3
Release:    1
Group:      System/Libraries
License:    LGPLv2.1
URL:        https://github.com/nemomobile/mthemedaemon
Source0:    %{name}-%{version}.tar.bz2
Source1:    mthemedaemon.desktop
Source2:    mthemedaemon.service
Source100:  mthemedaemon.yaml
Requires:   nemo-theme-default
Requires:   systemd
Requires:   systemd-user-session-targets
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig
BuildRequires:  pkgconfig(QtOpenGL)
BuildRequires:  pkgconfig(mlite)
BuildRequires:  pkgconfig(systemd)
BuildRequires:  fdupes


%description
Daemon for sharing theme pixmaps




%prep
%setup -q -n %{name}-%{version}

# >> setup
# << setup

%build
# >> build pre
# << build pre

%qmake 

make %{?jobs:-j%jobs}

# >> build post
# << build post
%install
rm -rf %{buildroot}
# >> install pre
# << install pre
%qmake_install
mkdir -p %{buildroot}%{_sysconfdir}/xdg/autostart
cp -a %{SOURCE1} %{buildroot}%{_sysconfdir}/xdg/autostart
mkdir -p %{buildroot}%{_libdir}/systemd/user/
cp -a %{SOURCE2} %{buildroot}%{_libdir}/systemd/user/

# >> install post
# Create the mthemedaemon cache directory
mkdir -p %{buildroot}/var/cache/meegotouch
mkdir -p %{buildroot}%{_libdir}/systemd/user/user-session.target.wants
ln -s ../mthemedaemon.service %{buildroot}%{_libdir}/systemd/user/user-session.target.wants/
# << install post

%fdupes  %{buildroot}/%{_datadir}

%post
/sbin/ldconfig
# >> post
if [ "$1" -ge 1 ]; then
systemctl-user daemon-reload || :
systemctl-user restart mthemedaemon.service || :
fi
# << post 

%postun
/sbin/ldconfig
# >> postun
if [ -d /var/cache/meegotouch ]; then
rm -rf /var/cache/meegotouch 
fi
if [ "$1" -eq 0 ]; then
systemctl-user stop mthemedaemon.service || :
systemctl-user daemon-reload || :
fi
# << postun


%files
%defattr(-,root,root,-)
%{_bindir}/mthemedaemon
%{_libdir}/systemd/user/mthemedaemon.service
%{_sysconfdir}/xdg/autostart/mthemedaemon.desktop
%{_sysconfdir}/meegotouch/themedaemonpriorities.conf
# >> files
%attr(1777, -, -) /var/cache/meegotouch
%{_libdir}/systemd/user/user-session.target.wants/mthemedaemon.service
# << files

