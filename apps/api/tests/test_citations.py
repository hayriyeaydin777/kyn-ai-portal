import pytest

from app.services.citation_validator import UnsupportedClaimError, validate_citations


def test_valid_citations_pass():
    validate_citations(["application.name"], {"application.name", "application.criticality"})


def test_unsupported_citation_raises():
    with pytest.raises(UnsupportedClaimError):
        validate_citations(["application.fabricated_field"], {"application.name"})


def test_empty_citations_always_pass():
    validate_citations([], {"application.name"})
