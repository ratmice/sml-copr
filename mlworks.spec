Name:		mlworks
Version:	messy_copr	
Release:	3%{?dist}
Summary:	mlworks messy bootstrap from an amalgamation of branches
Group:		Development/Languages
License:	BSD
URL:		https://www.ravenbrook.com/project/mlworks/
Source0:	https://github.com/ratmice/mlworks/archive/messy_copr.tar.gz

BuildRequires:	gcc elfutils-libelf-devel smlnj
BuildRequires:  motif-devel libX11-devel libXpm-devel libXext-devel
BuildRequires: /usr/include/gnu/stubs-32.h
BuildRequires: /lib/libgcc_s.so.1
Requires:	motif elfutils-libelf libX11 libXpm libXext	

%description
work in progress
# Not sure how to deal with architecture yet,
# hard codes i386, needs to uppercase arch to I386.
%prep
%setup -q -n %{name}-%{version}/src
ln -s i386/ machine
ln -s unix/ system
ln -s ../system/_os.sml main/
ln -s ../system/__os.sml main/

%build
make -C rts/ ARCH=I386 OS=Linux
sml <make/smlnj-boot.sml
make %{?_smp_mflags} -C images/I386/Linux/ OS=Linux ARCH=I386 batch.img
LD_LIBRARY_PATH=rts/bin/I386/Linux/ rts/bin/I386/Linux/main-g -MLWpass xx -load images/I386/Linux/batch.img xx -pervasive-dir pervasive/ -project xinterpreter.mlp -configuration I386/Linux -target xinterpreter.sml -build
make %{?_smp_mflags} -C images/I386/Linux/ OS=Linux ARCH=I386 guib.img
LD_LIBRARY_PATH=rts/bin/I386/Linux/ rts/bin/I386/Linux/main-g -MLWpass xx -load images/I386/Linux/batch.img xx -pervasive-dir pervasive/ -project interpreter.mlp -configuration I386/Linux -target interpreter.sml -build
make %{?_smp_mflags} -C images/I386/Linux/ OS=Linux ARCH=I386 tty.img
make %{?_smp_mflags} -C images/I386/Linux/ OS=Linux ARCH=I386 gui.img
make %{?_smp_mflags} -C images/I386/Linux/ OS=Linux ARCH=I386 ttyb.img

%install
mkdir -p %{buildroot}/%{_libdir}
mkdir -p %{buildroot}/opt/mlworks/{basis,motif,utils,foreign,system}
mkdir -p %{buildroot}/%{_bindir}
mkdir -p %{buildroot}/opt/mlworks/images/
mkdir -p %{buildroot}/opt/mlworks/objects/Release/
mkdir -p %{buildroot}/%{_datadir}/X11/app-defaults
mkdir -p %{buildroot}/opt/mlworks/pervasive/DEPEND

install -t %{buildroot}/opt/mlworks/images/ images/I386/Linux/*.img
install -T scripts/basis-unix.mlp %{buildroot}/opt/mlworks/basis/basis.mlp
install -t %{buildroot}/opt/mlworks/system unix/*.sml
install -t %{buildroot}/opt/mlworks/basis basis/*.sml
install -t %{buildroot}/opt/mlworks/basis unix/*.sml
install -t %{buildroot}/opt/mlworks/motif motif/*.{mlp,sml}
install -t %{buildroot}/opt/mlworks/utils utils/*.{mlp,sml}
cp -r foreign %{buildroot}/opt/mlworks/
install -t %{buildroot}/opt/mlworks/objects/Release ../objects/I386/Linux/Release/*.mo
install -t %{buildroot}/opt/mlworks/pervasive/DEPEND pervasive/DEPEND/*
install -t %{buildroot}/opt/mlworks/pervasive/ pervasive/*.mo

install -t %{buildroot}/%{_libdir} rts/bin/I386/Linux/*.so
for i in rts/bin/I386/Linux/*;
 do if [ -n $(basename $i | grep -v 'libml') ]; then 
	install -T $i %{buildroot}/%{_bindir}/mlworks-$(basename $i);
    fi
 done
install -t %{buildroot}/%{_datadir}/X11/app-defaults/	app-defaults/{MLWorks-color,MLWorks-normal-fonts,MLWorks-demo-fonts,MLWorks-proj-fonts,MLWorks-labels,MLWorks-mono}

cd ..
cp -r demo/ %{buildroot}/opt/mlworks/

%files
%{_bindir}/mlworks-*
%{_libdir}/*.so
%{_datadir}/X11/app-defaults/*
/opt/mlworks/
%doc

%changelog
* Thu Apr 12 2018 Matt Rice <ratmice@gmail.com> - messy_copr-3
- initial attempt
