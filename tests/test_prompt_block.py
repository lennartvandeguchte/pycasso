#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Unit tests for prompt_generation.py
import os

import pytest
import responses
from piblo.prompt_block import PromptBlock, QuoteBlock, FileBlock
from piblo.constants import UnitTestConst


def test_quote_block_str_representation():
    quote_block = QuoteBlock()
    assert str(quote_block) == "QuoteBlock()"
    assert repr(quote_block) == "QuoteBlock()"


@responses.activate
def test_quote_block_successful_response():
    quote_block = QuoteBlock()
    mock_response = [{"q": "Life is what happens while you are busy making other plans.", "a": "John Lennon"}]
    responses.add(
        responses.GET,
        "https://zenquotes.io/api/random",
        json=mock_response,
        status=200
    )

    result = quote_block.generate()
    expected = '"Life is what happens while you are busy making other plans." - John Lennon'
    assert result == expected


@responses.activate
def test_quote_block_empty_response():
    quote_block = QuoteBlock()
    responses.add(
        responses.GET,
        "https://zenquotes.io/api/random",
        json=[],
        status=200
    )

    result = quote_block.generate()
    assert result == ""


@responses.activate
def test_quote_block_invalid_response():
    quote_block = QuoteBlock()
    responses.add(
        responses.GET,
        "https://zenquotes.io/api/random",
        json={"error": "Invalid response"},
        status=200
    )

    result = quote_block.generate()
    assert result == ""


@responses.activate
def test_quote_block_timeout():
    quote_block = QuoteBlock()
    responses.add(
        responses.GET,
        "https://zenquotes.io/api/random",
        body=responses.ConnectionError()
    )

    result = quote_block.generate()
    assert result == ""


class MockPromptBlock(PromptBlock):
    def generate(self) -> str:
        return "test content"


def test_prompt_block_abstract():
    with pytest.raises(TypeError):
        PromptBlock()


def test_mock_prompt_block():
    block = MockPromptBlock()
    assert block.generate() == "test content"
    assert str(block) == "MockPromptBlock()"
    assert repr(block) == "MockPromptBlock()"


def test_file_block():
    block = FileBlock()
    file = os.path.join(os.path.dirname(__file__), UnitTestConst.PROMPT_BLOCK_FOLDER.value,
                        UnitTestConst.PROMPT_BLOCK_FILE.value)
    expected = "Test Block"
    assert block.generate(file) == expected


def test_file_block_not_found():
    block = FileBlock()
    file = os.path.join(os.path.dirname(__file__), UnitTestConst.PROMPT_BLOCK_FOLDER.value, "badfilepath.bad")
    expected = ""
    assert block.generate(file) == expected
