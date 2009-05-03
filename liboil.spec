#
# Conditional build:
%bcond_without	static_libs	# don't build static libraries
%bcond_without	tests		# don't perform "make check"
#
Summary:	Library of Optimized Inner Loops
Summary(pl.UTF-8):	Biblioteka zoptymalizowanych wewnętrznych pętli
Name:		liboil
Version:	0.3.16
Release:	1
Epoch:		1
License:	BSD
Group:		Libraries
Source0:	http://liboil.freedesktop.org/download/%{name}-%{version}.tar.gz
# Source0-md5:	febb1d9f9bc4c440fcf622dc90f8b6b7
Patch0:		%{name}-opt.patch
Patch1:		%{name}-fixes.patch
URL:		http://liboil.freedesktop.org/wiki/
BuildRequires:	autoconf >= 2.58
BuildRequires:	automake >= 1.6
BuildRequires:	glib2-devel >= 2.0
BuildRequires:	gtk-doc-automake
BuildRequires:	libtool
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.98
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# cannot remove frame pointers on ix86, SSE wrapper hack relies on
# gcc stack frames
#define		specflags	-fomit-frame-pointer
# CFLAGS_ALTIVEC are set, but not used
%define		specflags_ppc	-maltivec

%description
Liboil is a library of simple functions that are optimized for various
CPUs. These functions are generally loops implementing simple
algorithms, such as converting an array of N integers to
floating-poing numbers or multiplying and summing an array of N
numbers. Clearly such functions are candidates for significant
optimization using various techniques, especially by using extended
instructions provided by modern CPUs (Altivec, MMX, SSE, etc.).

Many multimedia applications and libraries already do similar things
internally. The goal of this project is to consolidate some of the
code used by various multimedia projects, and also make optimizations
easier to use by a broad range of applications.

%description -l pl.UTF-8
Liboil to biblioteka prostych funkcji zoptymalizowanych dla różnych
procesorów. Funkcje te to zwykle pętle implementujące proste
algorytmy, takie jak konwersja tablicy N liczb całkowitych na liczby
zmiennoprzecinkowe albo mnożenie i dodawanie tablicy N liczb. Takie
funkcje są kandydatami do znaczącej optymalizacji przy użyciu różnych
technik, szczególnie poprzez użycie rozszerzonych instrukcji
udostępnianych przez nowoczesne procesory (Altivec, MMX, SSE itp.).

Wiele aplikacji multimedialnych i bibliotek już robi takie rzeczy
wewnętrznie. Celem tego projektu jest połączenie części kodu używanego
przez różne projekty multimedialne i ułatwienie używania optymalizacji
w szerszym zakresie aplikacji.

%package devel
Summary:	Header files for liboil library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki liboil
Group:		Development/Libraries
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description devel
Header files for liboil library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki liboil.

%package static
Summary:	Static liboil library
Summary(pl.UTF-8):	Statyczna biblioteka liboil
Group:		Development/Libraries
Requires:	%{name}-devel = %{epoch}:%{version}-%{release}

%description static
Static liboil library.

%description static -l pl.UTF-8
Statyczna biblioteka liboil.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}

%configure \
	--with-html-dir=%{_gtkdocdir} \
	%{!?with_static_libs:--disable-static}

%{__make} -j1

%{?with_tests:%{__make} check}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__make} clean -C examples
cp -rf examples/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

rm -f $RPM_BUILD_ROOT%{_libdir}/liboiltmp1*

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING NEWS README
%attr(755,root,root) %{_libdir}/liboil-0.3.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/liboil-0.3.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/liboil-0.3.so
%{_libdir}/liboil-0.3.la
%{_includedir}/liboil-0.3
%{_pkgconfigdir}/liboil-0.3.pc
%{_gtkdocdir}/liboil
%{_examplesdir}/%{name}-%{version}

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/liboil-0.3.a
%endif
