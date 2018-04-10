Name:           smlnj
Version:        110.82
Release:        1%{?dist}
Summary:        Standard ML of New Jersey

Group:          Development/Languages
License:        MIT
URL:            http://www.smlnj.org/
                
Source0:        http://smlnj.cs.uchicago.edu/dist/working/%{version}/config.tgz
Source1:        http://smlnj.cs.uchicago.edu/dist/working/%{version}/cm.tgz
Source2:        http://smlnj.cs.uchicago.edu/dist/working/%{version}/compiler.tgz
Source3:        http://smlnj.cs.uchicago.edu/dist/working/%{version}/runtime.tgz
Source4:        http://smlnj.cs.uchicago.edu/dist/working/%{version}/system.tgz
Source5:        http://smlnj.cs.uchicago.edu/dist/working/%{version}/MLRISC.tgz
Source6:        http://smlnj.cs.uchicago.edu/dist/working/%{version}/smlnj-lib.tgz
Source7:        http://smlnj.cs.uchicago.edu/dist/working/%{version}/ckit.tgz
Source8:        http://smlnj.cs.uchicago.edu/dist/working/%{version}/nlffi.tgz
Source9:        http://smlnj.cs.uchicago.edu/dist/working/%{version}/cml.tgz
Source10:       http://smlnj.cs.uchicago.edu/dist/working/%{version}/eXene.tgz
Source11:       http://smlnj.cs.uchicago.edu/dist/working/%{version}/ml-lex.tgz
Source12:       http://smlnj.cs.uchicago.edu/dist/working/%{version}/ml-yacc.tgz
Source13:       http://smlnj.cs.uchicago.edu/dist/working/%{version}/ml-burg.tgz
Source14:       http://smlnj.cs.uchicago.edu/dist/working/%{version}/ml-lpt.tgz
Source15:       http://smlnj.cs.uchicago.edu/dist/working/%{version}/pgraph.tgz
Source16:       http://smlnj.cs.uchicago.edu/dist/working/%{version}/trace-debug-profile.tgz
Source17:       http://smlnj.cs.uchicago.edu/dist/working/%{version}/heap2asm.tgz
Source18:       http://smlnj.cs.uchicago.edu/dist/working/%{version}/smlnj-c.tgz
Source19:       http://smlnj.cs.uchicago.edu/dist/working/%{version}/boot.x86-unix.tgz
Source20:       http://smlnj.cs.uchicago.edu/dist/working/%{version}/boot.ppc-unix.tgz
Source21:       http://smlnj.cs.uchicago.edu/dist/working/%{version}/boot.sparc-unix.tgz
Source22:       http://smlnj.cs.uchicago.edu/dist/working/%{version}/%{version}-README.html

BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildRequires: /usr/include/gnu/stubs-32.h, /lib/libgcc_s.so.1

%global smlnj_bootstrap 1
%if !%{smlnj_bootstrap}
BuildRequires:  smlnj
%endif

%description
Standard ML of New Jersey (SML/NJ) is a compiler and programming environment
for the Standard ML programming language. It was originally developed jointly
at Bell Laboratories and Princeton University, and is now a joint project
between researchers at Bell Laboratories, Lucent Technologies), Princeton
University, Yale University (The FLINT Project), and AT&T Research.

%global debug_package %{nil}

%prep
%setup -q -T -c -a 0
cp %{SOURCE0} .
cp %{SOURCE1} .
cp %{SOURCE2} .
cp %{SOURCE3} .
cp %{SOURCE4} .
cp %{SOURCE5} .
cp %{SOURCE6} .
cp %{SOURCE7} .
cp %{SOURCE8} .
cp %{SOURCE9} .
cp %{SOURCE10} .
cp %{SOURCE11} .
cp %{SOURCE12} .
cp %{SOURCE13} .
cp %{SOURCE14} .
cp %{SOURCE15} .
cp %{SOURCE16} .
cp %{SOURCE17} .
cp %{SOURCE18} .
%if %{smlnj_bootstrap}
cp %{SOURCE19} .
cp %{SOURCE20} .
cp %{SOURCE21} .
%endif
cp %{SOURCE22} .



%build
%if !%{smlnj_bootstrap}
mkdir bootstrap
for file in system.tgz MLRISC.tgz cm.tgz compiler.tgz ml-yacc.tgz smlnj-lib.tgz pgraph.tgz; do
    tar -xzf $file -C bootstrap
done

pushd bootstrap/system

sed -i -e 's@\.\./\.\./@\.\./@g' pathconfig
echo 'CMB.make ();' | sml '$smlnj/cmb.cm'

sed -i -e 's@twoup=.*@twoup=%{_libdir}/smlnj@' makeml
./makeml

eval $(%{_libdir}/smlnj/bin/.arch-n-opsys)
tar -czf ../../boot.$ARCH-unix.tgz sml.boot.*

popd
%endif

cat > config/targets << 'EOF'
request ml-ulex
request ml-ulex-mllex-tool
request ml-lex
request ml-lex-lex-ext
request ml-yacc
request ml-yacc-grm-ext
request ml-antlr
request ml-lpt-lib
request ml-burg
request smlnj-lib
request pgraph-util
request tdp-util
request cml
request cml-lib
request eXene
request mlrisc
request ckit
request ml-nlffi-lib
request ml-nlffigen
request mlrisc-tools
request nowhere
request heap2asm
EOF

URLGETTER=true ./config/install.sh

# This can't be done in the prep section because
# the file is in a tarball.
sed -i \
    -e '1s@#!/usr/local/bin/perl@#!/usr/bin/perl@' \
    -e 's@require "mltex.thm";@do "mltex.thm" || die "$!";@' \
    MLRISC/Doc/html/mltex2html


%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_libdir}/smlnj
mv bin lib %{buildroot}%{_libdir}/smlnj

# Fix paths.
for file in %{buildroot}%{_libdir}/smlnj/bin/{*,.*}; do
    if [[ -f $file ]]; then
        sed -i \
            -e 's@BIN_DIR=".*"@BIN_DIR="%{_libdir}/smlnj/bin"@g' \
            -e 's@LIB_DIR=".*"@LIB_DIR="%{_libdir}/smlnj/lib"@g' \
            $file
    fi
done

# Fix permissions.
chmod 0755 %{buildroot}%{_libdir}/smlnj/bin/.arch-n-opsys 
chmod 0755 %{buildroot}%{_libdir}/smlnj/bin/.link-sml 
chmod 0755 %{buildroot}%{_libdir}/smlnj/bin/.run-sml 
chmod 0755 %{buildroot}%{_libdir}/smlnj/bin/.run/run.*-linux
chmod 0755 %{buildroot}%{_libdir}/smlnj/bin/heap2asm 
chmod 0755 %{buildroot}%{_libdir}/smlnj/bin/heap2exec 
chmod 0755 %{buildroot}%{_libdir}/smlnj/bin/ml-antlr 
chmod 0755 %{buildroot}%{_libdir}/smlnj/bin/ml-build 
chmod 0755 %{buildroot}%{_libdir}/smlnj/bin/ml-burg
chmod 0755 %{buildroot}%{_libdir}/smlnj/bin/ml-lex
chmod 0755 %{buildroot}%{_libdir}/smlnj/bin/ml-makedepend 
chmod 0755 %{buildroot}%{_libdir}/smlnj/bin/ml-nlffigen 
chmod 0755 %{buildroot}%{_libdir}/smlnj/bin/ml-ulex 
chmod 0755 %{buildroot}%{_libdir}/smlnj/bin/ml-yacc
chmod 0755 %{buildroot}%{_libdir}/smlnj/bin/nowhere 
chmod 0755 %{buildroot}%{_libdir}/smlnj/bin/sml

# Make wrapper scripts.
for file in %{buildroot}%{_libdir}/smlnj/bin/*; do
    cmd=$(basename $file)
    cat > %{buildroot}%{_bindir}/$cmd << EOF
#!/bin/sh
export SMLNJ_HOME="%{_libdir}/smlnj"
exec %{_libdir}/smlnj/bin/$cmd "\$@"
EOF
    chmod 0755 %{buildroot}%{_bindir}/$cmd
done

# Move docs into a separate directory.
mkdir -p docs/{cml,ml-lex,ml-lpt,MLRISC,ml-yacc,smlnj-lib}
mv cml/{doc,CHANGES,README,TODO} docs/cml
mv ml-lex/{README,*.doc,*.tex} docs/ml-lex
mv ml-lpt/{doc,README,TODO} docs/ml-lpt
mv MLRISC/Doc docs/MLRISC
chmod 0644 docs/MLRISC/Doc/html/mltex2html
mv ml-yacc/{doc,COPYRIGHT,README} docs/ml-yacc
mv smlnj-lib/{Doc,CHANGES,LICENSE,PORTING,README,TODO} docs/smlnj-lib

 
%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc %{version}-README.html docs/*
%{_bindir}/*
%{_libdir}/smlnj


%changelog
* Tue Apr 10 2018 Matt Rice <ratmice@gmail.com> - 110.82-1
- Upstream released a new version.

* Sun Nov 19 2017 John Southworth <john.southworth@gmail.com> - 110.80-1
- Update for Fedora 27

* Thu Nov 17 2016 John Southworth <john.southworth@gmail.com> - 110.80-1
- Upstream released a new version.

* Sun Jan 13 2013 Ricky Elrod <codeblock@fedoraproject.org> - 110.75-1
- Upstream released a new version.

* Mon May 30 2011 Ricky Zhou <ricky@fedoraproject.org> - 110.73-1
- Upstream released a new version.

* Fri Mar 12 2010 Ricky Zhou <ricky@fedoraproject.org> - 110.72-1
- Upstream released a new version.

* Sat Dec 05 2009 Ricky Zhou <ricky@fedoraproject.org> - 110.71-1
- Upstream released a new version.

* Fri May 29 2009 Ricky Zhou <ricky@fedoraproject.org> - 110.67-1
- Initial RPM Package.

