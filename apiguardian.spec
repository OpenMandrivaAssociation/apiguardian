Name:		apiguardian
Version:	1.1.2
Release:	1
Summary:	Annotation that publishes the stability of an API
Group:		Development/Java
License:	Apache-2.0
URL:		https://github.com/apiguardian-team/apiguardian
Source0:	https://github.com/apiguardian-team/apiguardian/archive/refs/tags/r%{version}.tar.gz#/apiguardian-%{version}.tar.gz
BuildArch:	noarch
BuildRequires:	python
BuildRequires:	maven
BuildRequires:	maven-components >= 3.10.0
BuildRequires:	java-current-devel
BuildSystem:	maven
BuildOption(install):	--file-name apiguardian-api

%description
@API Guardian annotates public types, methods, constructors, and
fields with a stability status. JUnit Platform and Jupiter use it.
1.1.2 is the current release. The project is a single annotation and
has no dependencies. The Gradle build is replaced with a parentless
Maven POM so the jar is installed as org.apiguardian:apiguardian-api.

%prep
%autosetup -n apiguardian-r%{version}
rm -rf .github gradle gradlew gradlew.bat settings.gradle.kts build.gradle.kts src/module
python - <<'PY'
import xml.etree.ElementTree as ET

NS = "http://maven.apache.org/POM/4.0.0"
ET.register_namespace("", NS)

def tag(name):
    return "{" + NS + "}" + name

def add(parent, name, text):
    node = ET.SubElement(parent, tag(name))
    node.text = text
    return node

root = ET.Element(tag("project"))
add(root, "modelVersion", "4.0.0")
add(root, "groupId", "org.apiguardian")
add(root, "artifactId", "apiguardian-api")
add(root, "version", "%{version}")
add(root, "name", "@API Guardian")
add(root, "description", "Annotation that publishes the stability of an API")
props = ET.SubElement(root, tag("properties"))
add(props, "maven.compiler.release", "8")
add(props, "project.build.sourceEncoding", "UTF-8")
ET.ElementTree(root).write("pom.xml", encoding="utf-8", xml_declaration=True)
PY

%build -a
printf 'Automatic-Module-Name: org.apiguardian.api\n' > manifest-extra.mf
jar ufm target/apiguardian-api-%{version}.jar manifest-extra.mf

%files -f .mfiles
%doc LICENSE README.md
