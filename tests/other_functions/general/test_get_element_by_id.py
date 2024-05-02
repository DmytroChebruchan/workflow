import unittest
from unittest.mock import Mock

from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from api.general.utils_element_class import ElementRepo
from core.models.node import Node


class TestFunctions(unittest.IsolatedAsyncioTestCase):

    async def test_get_elements(self, element=Node):
        # Create a mock session and result
        mock_session = Mock(spec=AsyncSession)
        mock_result = Mock(spec=Result)
        mock_result.scalars.return_value.all.return_value = [
            {"id": 1, "name": "element1"},
            {"id": 2, "name": "element2"},
        ]
        mock_session.execute.return_value = mock_result
        element = ElementRepo(session=mock_session, model=element)
        # Call the function
        elements = await element.get_elements()

        # Assert the function output
        self.assertEqual(
            elements,
            [{"id": 1, "name": "element1"}, {"id": 2, "name": "element2"}],
        )

        # Assert the function calls
        mock_session.execute.assert_called_once()
        mock_result.scalars.assert_called_once()
        mock_result.scalars.return_value.all.assert_called_once()
