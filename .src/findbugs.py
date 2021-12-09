#!/usr/bin/python3.8

import re, sys
import xml.dom.minidom as MD
import xml.etree.ElementTree as ET

def clean(xmlStr, header):
    xmlStr = re.sub('[\n|\t]', '', xmlStr)
    xmlStr = re.sub(' +', ' ', xmlStr)
    xmlStr = re.sub('> <', '><', xmlStr)
    xmlStr = re.sub(header, '<root>', xmlStr)
    xmlStr = re.sub('<\?xml*>', '', xmlStr)
    return re.sub('</project>', '</root>', xmlStr)

def addArtifactElemen(parent, arr):
    groupId = ET.SubElement(parent, "groupId")
    artifactId = ET.SubElement(parent, "artifactId")
    version = ET.SubElement(parent, "version")

    groupId.text = arr[0]
    artifactId.text = arr[1]
    version.text = arr[2]

def addPluginExecElemen(plugin, arr):
    executions = ET.SubElement(plugin, 'executions')
    execution = ET.SubElement(executions, 'execution')
    id = ET.SubElement(execution, 'id')
    phase = ET.SubElement(execution, 'phase')
    goals = ET.SubElement(execution, 'goals')
    goal = ET.SubElement(goals, 'goal')

    id.text = arr[0]
    phase.text = arr[1]
    goal.text = arr[2]

def addFindBugsPlugin(tree):
    root = tree.findall(".//plugins")[0]
    plugin = ET.SubElement(root, "plugin")
    addArtifactElemen(plugin, ['org.codehaus.mojo', 'findbugs-maven-plugin', '3.0.5'])

    config = ET.SubElement(plugin, "configuration")
    effort = ET.SubElement(config, "effort")
    failOnError = ET.SubElement(config, "failOnError")
    threshold = ET.SubElement(config, "threshold")
    xmlOutput = ET.SubElement(config, "xmlOutput")
    outputDir = ET.SubElement(config, "findbugsXmlOutputDirectory")

    effort.text = 'Max'
    failOnError.text = 'false'
    threshold.text = 'Low'
    xmlOutput.text = 'true'
    outputDir.text = '${project.build.directory}/findbugs'

    addPluginExecElemen(plugin, ['analysis-compile', 'compile', 'check'])

def addXMLTransformPlugin(tree):
	root = tree.findall(".//plugins")[0]
	plugin = ET.SubElement(root, "plugin")
	addArtifactElemen(plugin, ['org.codehaus.mojo', 'xml-maven-plugin', '1.0'])

	config = ET.SubElement(plugin, "configuration")
	transSets = ET.SubElement(config, "transformationSets")
	transSet = ET.SubElement(transSets, "transformationSet")
	inputDir = ET.SubElement(transSet, 'dir')
	outputDir = ET.SubElement(transSet, "outputDir")
	stylesheet = ET.SubElement(transSet, "stylesheet")

	fileMappers = ET.SubElement(transSet, "fileMappers")
	fileMapper = ET.SubElement(fileMappers, "fileMapper")
	targetExtension = ET.SubElement(fileMapper, "targetExtension")

	inputDir.text = '${project.build.directory}/findbugs'
	outputDir.text = '${project.build.directory}/findbugs'
	stylesheet.text = 'default.xsl'
	fileMapper.set('implementation', "org.codehaus.plexus.components.io.filemappers.FileExtensionMapper")
	targetExtension.text = ".html"

	addPluginExecElemen(plugin, ['transform-compile', 'compile', 'transform'])
	deps = ET.SubElement(plugin, 'dependencies')
	dep = ET.SubElement(deps, 'dependency')
	addArtifactElemen(dep, ['com.google.code.findbugs', 'findbugs', '2.0.1'])

def redoDir(lst, idx, repl):
    del lst[idx]
    lst.insert(idx, repl)

def main():
	tree = None
	header="""<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">"""
	with open(sys.argv[1], encoding='utf-8') as f:
		xmlStr = f.readlines()
		redoDir(xmlStr, 0, """<?xml version="1.0" ?>""")
		redoDir(xmlStr, 1, header)
		xmlStr = clean("".join(xmlStr), header)
		tree = ET.fromstring(xmlStr)
		addFindBugsPlugin(tree)
		addXMLTransformPlugin(tree)

	xmlstr = MD.parseString(ET.tostring(tree)).toprettyxml(indent="   ")
	with open(sys.argv[1], "w") as f:
		xmlstr = xmlstr.replace('<root>', header).replace('</root>', '</project>')
		f.write(xmlstr)

if __name__ == '__main__':
    main()
