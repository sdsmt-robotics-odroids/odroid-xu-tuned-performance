Name:           odroid-xu-tuned-performance
Version:        0.1.0
Release:        1%{?dist}
Summary:        Performance profile for CPU governing

Group:          System Environment/Base
License:        BSD
URL:            http://odroid.com/dokuwiki/doku.php?id=en:odroid-xu
Source0:        tuned.conf

BuildArch:      noarch

Requires:       tuned
Requires(post): systemd
Requires(postun): systemd

%description
This package configures tuned to keep the CPUs governors in performance
mode.

%prep

%build

%install
install -p -m0644 -D %{SOURCE0} %{buildroot}%{_sysconfdir}/tuned/odroid-xu-performance/tuned.conf

%post
# NOTE: If the profile name ever changes, that will need to be handled here
# for upgrade scenario

# If no other profile is active, make us active
grep -q ".*" %{_sysconfdir}/tuned/active_profile || (set -e
  echo "odroid-xu-performance" > %{_sysconfdir}/tuned/active_profile
  systemctl try-restart tuned.service
)

%preun
# Only if we're uninstalling (and not upgrading)
if [$1 -eq 0 ]; then
  # If we're the active profile, remove us
  grep -q "^odroid-xu-performance$" %{_sysconfdir}/tuned/active_profile && (set -e
    echo -n "" > %{_sysconfdir}/tuned/active_profile
    systemctl try-restart tuned.service
  )
fi

%files
%dir %{_sysconfdir}/tuned/odroid-xu-performance/
%config(noreplace) %{_sysconfdir}/tuned/odroid-xu-performance/tuned.conf

%changelog
* Sat Apr 04 2015 Scott K Logan <logans@cottsay.net> - 0.1.0-1
- Initial package
