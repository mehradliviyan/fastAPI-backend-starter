from backend.shared_kernel.exceptions import AppError


class SampleBusinessError(AppError):
    code = "sample_business_error"
    message = "A sample business rule failed."


def test_app_error_exposes_stable_error_contract() -> None:
    error = SampleBusinessError(details={"field": "sample"})

    assert error.code == "sample_business_error"
    assert error.message == "A sample business rule failed."
    assert error.details == {"field": "sample"}
    assert str(error) == "A sample business rule failed."