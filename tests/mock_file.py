async def true_returner_mock(*args, **kwargs):
    return True


async def run_workflow_mock(*args, **kwargs):
    return "Hello"


async def test_workflow_mock(*args, **kwargs):
    return {"id": 1, "title": "some"}
