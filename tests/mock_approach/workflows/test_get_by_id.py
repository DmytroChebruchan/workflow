import unittest
from unittest.mock import Mock
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from api.general.utils import get_elements, get_element_by_id
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

        # Call the function
        elements = await get_elements(mock_session, element)

        # Assert the function output
        self.assertEqual(
            elements,
            [{"id": 1, "name": "element1"}, {"id": 2, "name": "element2"}],
        )

        # Assert the function calls
        mock_session.execute.assert_called_once()
        mock_result.scalars.assert_called_once()
        mock_result.scalars.return_value.all.assert_called_once()

    async def test_get_element_by_id(self, element=Node):
        # Create a mock session and mapper
        mock_session = Mock(spec=AsyncSession)
        mock_session.get.return_value = {"id": 1, "name": "element1"}

        # Call the function
        element_result = await get_element_by_id(mock_session, 1, element)

        # Assert the function output
        self.assertEqual(element_result, {"id": 1, "name": "element1"})

        # Assert the function calls
        mock_session.get.assert_called_once_with(element, 1)


if __name__ == "__main__":
    unittest.main()
