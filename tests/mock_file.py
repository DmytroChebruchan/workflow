async def true_returner(*args, **kwargs) -> True:
    return True


async def run_workflow_mock(*args, **kwargs):
    return "Hello"
