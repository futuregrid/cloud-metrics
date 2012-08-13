#!/usr/bin/env python

#
# Generated Sat Aug 11 13:45:04 2012 by generateDS.py version 2.7c.
#

import sys

import AmieUsageRecord as supermod

etree_ = None
Verbose_import_ = False
(   XMLParser_import_none, XMLParser_import_lxml,
    XMLParser_import_elementtree
    ) = range(3)
XMLParser_import_library = None
try:
    # lxml
    from lxml import etree as etree_
    XMLParser_import_library = XMLParser_import_lxml
    if Verbose_import_:
        print("running with lxml.etree")
except ImportError:
    try:
        # cElementTree from Python 2.5+
        import xml.etree.cElementTree as etree_
        XMLParser_import_library = XMLParser_import_elementtree
        if Verbose_import_:
            print("running with cElementTree on Python 2.5+")
    except ImportError:
        try:
            # ElementTree from Python 2.5+
            import xml.etree.ElementTree as etree_
            XMLParser_import_library = XMLParser_import_elementtree
            if Verbose_import_:
                print("running with ElementTree on Python 2.5+")
        except ImportError:
            try:
                # normal cElementTree install
                import cElementTree as etree_
                XMLParser_import_library = XMLParser_import_elementtree
                if Verbose_import_:
                    print("running with cElementTree")
            except ImportError:
                try:
                    # normal ElementTree install
                    import elementtree.ElementTree as etree_
                    XMLParser_import_library = XMLParser_import_elementtree
                    if Verbose_import_:
                        print("running with ElementTree")
                except ImportError:
                    raise ImportError("Failed to import ElementTree from any known place")

def parsexml_(*args, **kwargs):
    if (XMLParser_import_library == XMLParser_import_lxml and
        'parser' not in kwargs):
        # Use the lxml ElementTree compatible parser so that, e.g.,
        #   we ignore comments.
        kwargs['parser'] = etree_.ETCompatXMLParser()
    doc = etree_.parse(*args, **kwargs)
    return doc

#
# Globals
#

ExternalEncoding = 'ascii'

#
# Data representation classes
#

class UsageRecordTypeSub(supermod.UsageRecordType):
    def __init__(self, RecordIdentity=None, JobIdentity=None, UserIdentity=None, JobName=None, Charge=None, Status=None, Disk=None, Memory=None, Swap=None, Network=None, TimeDuration=None, TimeInstant=None, ServiceLevel=None, WallDuration=None, CpuDuration=None, NodeCount=None, Processors=None, EndTime=None, StartTime=None, MachineName=None, SubmitHost=None, Queue=None, ProjectName=None, Host=None, PhaseResource=None, VolumeResource=None, Resource=None, ConsumableResource=None, extensiontype_=None):
        super(UsageRecordTypeSub, self).__init__(RecordIdentity, JobIdentity, UserIdentity, JobName, Charge, Status, Disk, Memory, Swap, Network, TimeDuration, TimeInstant, ServiceLevel, WallDuration, CpuDuration, NodeCount, Processors, EndTime, StartTime, MachineName, SubmitHost, Queue, ProjectName, Host, PhaseResource, VolumeResource, Resource, ConsumableResource, extensiontype_, )
supermod.UsageRecordType.subclass = UsageRecordTypeSub
# end class UsageRecordTypeSub


class JobUsageRecordSub(supermod.JobUsageRecord):
    def __init__(self, RecordIdentity=None, JobIdentity=None, UserIdentity=None, JobName=None, Charge=None, Status=None, Disk=None, Memory=None, Swap=None, Network=None, TimeDuration=None, TimeInstant=None, ServiceLevel=None, WallDuration=None, CpuDuration=None, NodeCount=None, Processors=None, EndTime=None, StartTime=None, MachineName=None, SubmitHost=None, Queue=None, ProjectName=None, Host=None, PhaseResource=None, VolumeResource=None, Resource=None, ConsumableResource=None):
        super(JobUsageRecordSub, self).__init__(RecordIdentity, JobIdentity, UserIdentity, JobName, Charge, Status, Disk, Memory, Swap, Network, TimeDuration, TimeInstant, ServiceLevel, WallDuration, CpuDuration, NodeCount, Processors, EndTime, StartTime, MachineName, SubmitHost, Queue, ProjectName, Host, PhaseResource, VolumeResource, Resource, ConsumableResource, )
supermod.JobUsageRecord.subclass = JobUsageRecordSub
# end class JobUsageRecordSub


class UsageRecordsSub(supermod.UsageRecords):
    def __init__(self, Usage=None):
        super(UsageRecordsSub, self).__init__(Usage, )
supermod.UsageRecords.subclass = UsageRecordsSub
# end class UsageRecordsSub


class NetworkSub(supermod.Network):
    def __init__(self, storageUnit=None, metric='total', description=None, phaseUnit=None, valueOf_=None):
        super(NetworkSub, self).__init__(storageUnit, metric, description, phaseUnit, valueOf_, )
supermod.Network.subclass = NetworkSub
# end class NetworkSub


class DiskSub(supermod.Disk):
    def __init__(self, storageUnit=None, metric='total', type_=None, description=None, phaseUnit=None, valueOf_=None):
        super(DiskSub, self).__init__(storageUnit, metric, type_, description, phaseUnit, valueOf_, )
supermod.Disk.subclass = DiskSub
# end class DiskSub


class MemorySub(supermod.Memory):
    def __init__(self, storageUnit=None, metric='total', type_=None, description=None, phaseUnit=None, valueOf_=None):
        super(MemorySub, self).__init__(storageUnit, metric, type_, description, phaseUnit, valueOf_, )
supermod.Memory.subclass = MemorySub
# end class MemorySub


class SwapSub(supermod.Swap):
    def __init__(self, storageUnit=None, metric='total', type_=None, description=None, phaseUnit=None, valueOf_=None):
        super(SwapSub, self).__init__(storageUnit, metric, type_, description, phaseUnit, valueOf_, )
supermod.Swap.subclass = SwapSub
# end class SwapSub


class NodeCountSub(supermod.NodeCount):
    def __init__(self, metric='total', description=None, valueOf_=None):
        super(NodeCountSub, self).__init__(metric, description, valueOf_, )
supermod.NodeCount.subclass = NodeCountSub
# end class NodeCountSub


class ProcessorsSub(supermod.Processors):
    def __init__(self, consumptionRate=None, metric=None, description=None, valueOf_=None):
        super(ProcessorsSub, self).__init__(consumptionRate, metric, description, valueOf_, )
supermod.Processors.subclass = ProcessorsSub
# end class ProcessorsSub


class TimeDurationSub(supermod.TimeDuration):
    def __init__(self, type_=None, valueOf_=None):
        super(TimeDurationSub, self).__init__(type_, valueOf_, )
supermod.TimeDuration.subclass = TimeDurationSub
# end class TimeDurationSub


class TimeInstantSub(supermod.TimeInstant):
    def __init__(self, type_=None, valueOf_=None):
        super(TimeInstantSub, self).__init__(type_, valueOf_, )
supermod.TimeInstant.subclass = TimeInstantSub
# end class TimeInstantSub


class ServiceLevelSub(supermod.ServiceLevel):
    def __init__(self, type_=None, valueOf_=None):
        super(ServiceLevelSub, self).__init__(type_, valueOf_, )
supermod.ServiceLevel.subclass = ServiceLevelSub
# end class ServiceLevelSub


class CpuDurationSub(supermod.CpuDuration):
    def __init__(self, usageType=None, description=None, valueOf_=None):
        super(CpuDurationSub, self).__init__(usageType, description, valueOf_, )
supermod.CpuDuration.subclass = CpuDurationSub
# end class CpuDurationSub


class WallDurationSub(supermod.WallDuration):
    def __init__(self, description=None, valueOf_=None):
        super(WallDurationSub, self).__init__(description, valueOf_, )
supermod.WallDuration.subclass = WallDurationSub
# end class WallDurationSub


class EndTimeSub(supermod.EndTime):
    def __init__(self, description=None, valueOf_=None):
        super(EndTimeSub, self).__init__(description, valueOf_, )
supermod.EndTime.subclass = EndTimeSub
# end class EndTimeSub


class StartTimeSub(supermod.StartTime):
    def __init__(self, description=None, valueOf_=None):
        super(StartTimeSub, self).__init__(description, valueOf_, )
supermod.StartTime.subclass = StartTimeSub
# end class StartTimeSub


class MachineNameSub(supermod.MachineName):
    def __init__(self, description=None, valueOf_=None):
        super(MachineNameSub, self).__init__(description, valueOf_, )
supermod.MachineName.subclass = MachineNameSub
# end class MachineNameSub


class SubmitHostSub(supermod.SubmitHost):
    def __init__(self, description=None, valueOf_=None):
        super(SubmitHostSub, self).__init__(description, valueOf_, )
supermod.SubmitHost.subclass = SubmitHostSub
# end class SubmitHostSub


class HostSub(supermod.Host):
    def __init__(self, description=None, primary=False, valueOf_=None):
        super(HostSub, self).__init__(description, primary, valueOf_, )
supermod.Host.subclass = HostSub
# end class HostSub


class QueueSub(supermod.Queue):
    def __init__(self, description=None, valueOf_=None):
        super(QueueSub, self).__init__(description, valueOf_, )
supermod.Queue.subclass = QueueSub
# end class QueueSub


class JobNameSub(supermod.JobName):
    def __init__(self, description=None, valueOf_=None):
        super(JobNameSub, self).__init__(description, valueOf_, )
supermod.JobName.subclass = JobNameSub
# end class JobNameSub


class ProjectNameSub(supermod.ProjectName):
    def __init__(self, description=None, valueOf_=None):
        super(ProjectNameSub, self).__init__(description, valueOf_, )
supermod.ProjectName.subclass = ProjectNameSub
# end class ProjectNameSub


class StatusSub(supermod.Status):
    def __init__(self, description=None, valueOf_=None):
        super(StatusSub, self).__init__(description, valueOf_, )
supermod.Status.subclass = StatusSub
# end class StatusSub


class ChargeSub(supermod.Charge):
    def __init__(self, formula=None, description=None, unit=None, valueOf_=None):
        super(ChargeSub, self).__init__(formula, description, unit, valueOf_, )
supermod.Charge.subclass = ChargeSub
# end class ChargeSub


class JobIdentitySub(supermod.JobIdentity):
    def __init__(self, GlobalJobId=None, LocalJobId=None, ProcessId=None):
        super(JobIdentitySub, self).__init__(GlobalJobId, LocalJobId, ProcessId, )
supermod.JobIdentity.subclass = JobIdentitySub
# end class JobIdentitySub


class UserIdentitySub(supermod.UserIdentity):
    def __init__(self, LocalUserId=None, KeyInfo=None):
        super(UserIdentitySub, self).__init__(LocalUserId, KeyInfo, )
supermod.UserIdentity.subclass = UserIdentitySub
# end class UserIdentitySub


class RecordIdentitySub(supermod.RecordIdentity):
    def __init__(self, recordId=None, createTime=None, KeyInfo=None):
        super(RecordIdentitySub, self).__init__(recordId, createTime, KeyInfo, )
supermod.RecordIdentity.subclass = RecordIdentitySub
# end class RecordIdentitySub


class ConsumableResourceTypeSub(supermod.ConsumableResourceType):
    def __init__(self, units=None, description=None, valueOf_=None, extensiontype_=None):
        super(ConsumableResourceTypeSub, self).__init__(units, description, valueOf_, extensiontype_, )
supermod.ConsumableResourceType.subclass = ConsumableResourceTypeSub
# end class ConsumableResourceTypeSub


class ResourceTypeSub(supermod.ResourceType):
    def __init__(self, description=None, valueOf_=None):
        super(ResourceTypeSub, self).__init__(description, valueOf_, )
supermod.ResourceType.subclass = ResourceTypeSub
# end class ResourceTypeSub


class SignatureTypeSub(supermod.SignatureType):
    def __init__(self, Id=None, SignedInfo=None, SignatureValue=None, KeyInfo=None, Object=None):
        super(SignatureTypeSub, self).__init__(Id, SignedInfo, SignatureValue, KeyInfo, Object, )
supermod.SignatureType.subclass = SignatureTypeSub
# end class SignatureTypeSub


class SignatureValueTypeSub(supermod.SignatureValueType):
    def __init__(self, Id=None, valueOf_=None):
        super(SignatureValueTypeSub, self).__init__(Id, valueOf_, )
supermod.SignatureValueType.subclass = SignatureValueTypeSub
# end class SignatureValueTypeSub


class SignedInfoTypeSub(supermod.SignedInfoType):
    def __init__(self, Id=None, CanonicalizationMethod=None, SignatureMethod=None, Reference=None):
        super(SignedInfoTypeSub, self).__init__(Id, CanonicalizationMethod, SignatureMethod, Reference, )
supermod.SignedInfoType.subclass = SignedInfoTypeSub
# end class SignedInfoTypeSub


class CanonicalizationMethodTypeSub(supermod.CanonicalizationMethodType):
    def __init__(self, Algorithm=None, anytypeobjs_=None, valueOf_=None, mixedclass_=None, content_=None):
        super(CanonicalizationMethodTypeSub, self).__init__(Algorithm, anytypeobjs_, valueOf_, mixedclass_, content_, )
supermod.CanonicalizationMethodType.subclass = CanonicalizationMethodTypeSub
# end class CanonicalizationMethodTypeSub


class SignatureMethodTypeSub(supermod.SignatureMethodType):
    def __init__(self, Algorithm=None, HMACOutputLength=None, anytypeobjs_=None, valueOf_=None, mixedclass_=None, content_=None):
        super(SignatureMethodTypeSub, self).__init__(Algorithm, HMACOutputLength, anytypeobjs_, valueOf_, mixedclass_, content_, )
supermod.SignatureMethodType.subclass = SignatureMethodTypeSub
# end class SignatureMethodTypeSub


class ReferenceTypeSub(supermod.ReferenceType):
    def __init__(self, Type=None, Id=None, URI=None, Transforms=None, DigestMethod=None, DigestValue=None):
        super(ReferenceTypeSub, self).__init__(Type, Id, URI, Transforms, DigestMethod, DigestValue, )
supermod.ReferenceType.subclass = ReferenceTypeSub
# end class ReferenceTypeSub


class TransformsTypeSub(supermod.TransformsType):
    def __init__(self, Transform=None):
        super(TransformsTypeSub, self).__init__(Transform, )
supermod.TransformsType.subclass = TransformsTypeSub
# end class TransformsTypeSub


class TransformTypeSub(supermod.TransformType):
    def __init__(self, Algorithm=None, anytypeobjs_=None, XPath=None, valueOf_=None, mixedclass_=None, content_=None):
        super(TransformTypeSub, self).__init__(Algorithm, anytypeobjs_, XPath, valueOf_, mixedclass_, content_, )
supermod.TransformType.subclass = TransformTypeSub
# end class TransformTypeSub


class DigestMethodTypeSub(supermod.DigestMethodType):
    def __init__(self, Algorithm=None, anytypeobjs_=None, valueOf_=None, mixedclass_=None, content_=None):
        super(DigestMethodTypeSub, self).__init__(Algorithm, anytypeobjs_, valueOf_, mixedclass_, content_, )
supermod.DigestMethodType.subclass = DigestMethodTypeSub
# end class DigestMethodTypeSub


class KeyInfoTypeSub(supermod.KeyInfoType):
    def __init__(self, Id=None, KeyName=None, KeyValue=None, RetrievalMethod=None, X509Data=None, PGPData=None, SPKIData=None, MgmtData=None, anytypeobjs_=None, valueOf_=None, mixedclass_=None, content_=None):
        super(KeyInfoTypeSub, self).__init__(Id, KeyName, KeyValue, RetrievalMethod, X509Data, PGPData, SPKIData, MgmtData, anytypeobjs_, valueOf_, mixedclass_, content_, )
supermod.KeyInfoType.subclass = KeyInfoTypeSub
# end class KeyInfoTypeSub


class KeyValueTypeSub(supermod.KeyValueType):
    def __init__(self, DSAKeyValue=None, RSAKeyValue=None, anytypeobjs_=None, valueOf_=None, mixedclass_=None, content_=None):
        super(KeyValueTypeSub, self).__init__(DSAKeyValue, RSAKeyValue, anytypeobjs_, valueOf_, mixedclass_, content_, )
supermod.KeyValueType.subclass = KeyValueTypeSub
# end class KeyValueTypeSub


class RetrievalMethodTypeSub(supermod.RetrievalMethodType):
    def __init__(self, Type=None, URI=None, Transforms=None):
        super(RetrievalMethodTypeSub, self).__init__(Type, URI, Transforms, )
supermod.RetrievalMethodType.subclass = RetrievalMethodTypeSub
# end class RetrievalMethodTypeSub


class X509DataTypeSub(supermod.X509DataType):
    def __init__(self, X509IssuerSerial=None, X509SKI=None, X509SubjectName=None, X509Certificate=None, X509CRL=None, anytypeobjs_=None):
        super(X509DataTypeSub, self).__init__(X509IssuerSerial, X509SKI, X509SubjectName, X509Certificate, X509CRL, anytypeobjs_, )
supermod.X509DataType.subclass = X509DataTypeSub
# end class X509DataTypeSub


class X509IssuerSerialTypeSub(supermod.X509IssuerSerialType):
    def __init__(self, X509IssuerName=None, X509SerialNumber=None):
        super(X509IssuerSerialTypeSub, self).__init__(X509IssuerName, X509SerialNumber, )
supermod.X509IssuerSerialType.subclass = X509IssuerSerialTypeSub
# end class X509IssuerSerialTypeSub


class PGPDataTypeSub(supermod.PGPDataType):
    def __init__(self, PGPKeyID=None, PGPKeyPacket=None, anytypeobjs_=None):
        super(PGPDataTypeSub, self).__init__(PGPKeyID, PGPKeyPacket, anytypeobjs_, anytypeobjs_, )
supermod.PGPDataType.subclass = PGPDataTypeSub
# end class PGPDataTypeSub


class SPKIDataTypeSub(supermod.SPKIDataType):
    def __init__(self, SPKISexp=None, anytypeobjs_=None):
        super(SPKIDataTypeSub, self).__init__(SPKISexp, anytypeobjs_, )
supermod.SPKIDataType.subclass = SPKIDataTypeSub
# end class SPKIDataTypeSub


class ObjectTypeSub(supermod.ObjectType):
    def __init__(self, MimeType=None, Id=None, Encoding=None, anytypeobjs_=None, valueOf_=None, mixedclass_=None, content_=None):
        super(ObjectTypeSub, self).__init__(MimeType, Id, Encoding, anytypeobjs_, valueOf_, mixedclass_, content_, )
supermod.ObjectType.subclass = ObjectTypeSub
# end class ObjectTypeSub


class ManifestTypeSub(supermod.ManifestType):
    def __init__(self, Id=None, Reference=None):
        super(ManifestTypeSub, self).__init__(Id, Reference, )
supermod.ManifestType.subclass = ManifestTypeSub
# end class ManifestTypeSub


class SignaturePropertiesTypeSub(supermod.SignaturePropertiesType):
    def __init__(self, Id=None, SignatureProperty=None):
        super(SignaturePropertiesTypeSub, self).__init__(Id, SignatureProperty, )
supermod.SignaturePropertiesType.subclass = SignaturePropertiesTypeSub
# end class SignaturePropertiesTypeSub


class SignaturePropertyTypeSub(supermod.SignaturePropertyType):
    def __init__(self, Target=None, Id=None, anytypeobjs_=None, valueOf_=None, mixedclass_=None, content_=None):
        super(SignaturePropertyTypeSub, self).__init__(Target, Id, anytypeobjs_, valueOf_, mixedclass_, content_, )
supermod.SignaturePropertyType.subclass = SignaturePropertyTypeSub
# end class SignaturePropertyTypeSub


class DSAKeyValueTypeSub(supermod.DSAKeyValueType):
    def __init__(self, P=None, Q=None, G=None, Y=None, J=None, Seed=None, PgenCounter=None):
        super(DSAKeyValueTypeSub, self).__init__(P, Q, G, Y, J, Seed, PgenCounter, )
supermod.DSAKeyValueType.subclass = DSAKeyValueTypeSub
# end class DSAKeyValueTypeSub


class RSAKeyValueTypeSub(supermod.RSAKeyValueType):
    def __init__(self, Modulus=None, Exponent=None):
        super(RSAKeyValueTypeSub, self).__init__(Modulus, Exponent, )
supermod.RSAKeyValueType.subclass = RSAKeyValueTypeSub
# end class RSAKeyValueTypeSub


class VolumeResourceSub(supermod.VolumeResource):
    def __init__(self, units=None, description=None, storageUnit=None):
        super(VolumeResourceSub, self).__init__(units, description, storageUnit, )
supermod.VolumeResource.subclass = VolumeResourceSub
# end class VolumeResourceSub


class PhaseResourceSub(supermod.PhaseResource):
    def __init__(self, units=None, description=None, phaseUnit=None):
        super(PhaseResourceSub, self).__init__(units, description, phaseUnit, )
supermod.PhaseResource.subclass = PhaseResourceSub
# end class PhaseResourceSub



def get_root_tag(node):
    tag = supermod.Tag_pattern_.match(node.tag).groups()[-1]
    rootClass = None
    if hasattr(supermod, tag):
        rootClass = getattr(supermod, tag)
    return tag, rootClass


def parse(inFilename):
    doc = parsexml_(inFilename)
    rootNode = doc.getroot()
    rootTag, rootClass = get_root_tag(rootNode)
    if rootClass is None:
        rootTag = 'UsageRecordType'
        rootClass = supermod.UsageRecordType
    rootObj = rootClass.factory()
    rootObj.build(rootNode)
    # Enable Python to collect the space used by the DOM.
    doc = None
    sys.stdout.write('<?xml version="1.0" ?>\n')
    rootObj.export(sys.stdout, 0, name_=rootTag,
        namespacedef_='',
        pretty_print=True)
    doc = None
    return rootObj


def parseString(inString):
    from StringIO import StringIO
    doc = parsexml_(StringIO(inString))
    rootNode = doc.getroot()
    rootTag, rootClass = get_root_tag(rootNode)
    if rootClass is None:
        rootTag = 'UsageRecordType'
        rootClass = supermod.UsageRecordType
    rootObj = rootClass.factory()
    rootObj.build(rootNode)
    # Enable Python to collect the space used by the DOM.
    doc = None
    sys.stdout.write('<?xml version="1.0" ?>\n')
    rootObj.export(sys.stdout, 0, name_=rootTag,
        namespacedef_='')
    return rootObj


def parseLiteral(inFilename):
    doc = parsexml_(inFilename)
    rootNode = doc.getroot()
    rootTag, rootClass = get_root_tag(rootNode)
    if rootClass is None:
        rootTag = 'UsageRecordType'
        rootClass = supermod.UsageRecordType
    rootObj = rootClass.factory()
    rootObj.build(rootNode)
    # Enable Python to collect the space used by the DOM.
    doc = None
    sys.stdout.write('#from AmieUsageRecord import *\n\n')
    sys.stdout.write('import AmieUsageRecord as model_\n\n')
    sys.stdout.write('rootObj = model_.UsageRecordType(\n')
    rootObj.exportLiteral(sys.stdout, 0, name_="UsageRecordType")
    sys.stdout.write(')\n')
    return rootObj


USAGE_TEXT = """
Usage: python ???.py <infilename>
"""

def usage():
    print USAGE_TEXT
    sys.exit(1)


def main():
    args = sys.argv[1:]
    if len(args) != 1:
        usage()
    infilename = args[0]
    root = parse(infilename)


if __name__ == '__main__':
    #import pdb; pdb.set_trace()
    main()


