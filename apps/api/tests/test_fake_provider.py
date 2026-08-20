from app.providers.fake import FakeProvider
from app.services.evidence_bundle import EvidenceBundle


def _bundle() -> EvidenceBundle:
    return EvidenceBundle(
        application={
            "name": "Northstar Claims Service",
            "description": "Fictional claims platform.",
            "business_owner": "Demo Owner",
            "criticality": "high",
        },
        dependencies=[{"name": "Synthetic Identity Provider", "dependency_type": "auth", "criticality": "high"}],
        findings=[{"rule_id": "R002", "severity": "High", "message": "No failover documented."}],
    )


def test_fake_provider_is_deterministic():
    provider = FakeProvider()
    bundle = _bundle()

    first = provider.generate("brief", bundle)
    second = provider.generate("brief", bundle)

    assert first == second


def test_fake_provider_citations_are_subset_of_available_fields():
    provider = FakeProvider()
    bundle = _bundle()

    response = provider.generate("brief", bundle)

    assert set(response.citations).issubset(bundle.available_fields())
    assert "Northstar Claims Service" in response.text


def test_fake_provider_handles_empty_dependencies_and_findings():
    provider = FakeProvider()
    bundle = EvidenceBundle(application={"name": "Atlas Messaging Service", "criticality": "medium"})

    response = provider.generate("brief", bundle)

    assert "No dependencies documented" in response.text
    assert "No findings recorded" in response.text
