# libraries
import pytest

import chip8.presenter as presenter


# code
def test_(mocker):
    # arrange
    mocker.patch("chip8.model.vm.VirtualMachine")

    mock_get_view = mocker.patch("chip8.presenter.get_view")
    mock_view = mocker.patch("chip8.view.View")

    mock_get_view.side_effect = lambda: mock_view

    pre = presenter.Presenter()

    # act
    pre.run()

    # assert
    mock_view.run.assert_called_once()
