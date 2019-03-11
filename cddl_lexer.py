import re

from pygments.lexer import RegexLexer, bygroups, include, words
from pygments.token import (
    Comment,
    Keyword,
    Name,
    Number,
    Operator,
    Punctuation,
    String,
    Text,
)


class CddlLexer(RegexLexer):
    name = "CDDL"
    aliases = ["cddl"]
    filenames = ["*.cddl"]
    mimetypes = ["text/x-cddl"]

    _prelude_types = [
        "any",
        "b64legacy",
        "b64url",
        "bigfloat",
        "bigint",
        "bignint",
        "biguint",
        "bool",
        "bstr",
        "bytes",
        "cbor-any",
        "decfrac",
        "eb16",
        "eb64legacy",
        "eb64url",
        "encoded-cbor",
        "false",
        "float",
        "float16",
        "float16-32",
        "float32",
        "float32-64",
        "float64",
        "int",
        "integer",
        "mime-message",
        "nil",
        "nint",
        "null",
        "number",
        "regexp",
        "tdate",
        "text",
        "time",
        "true",
        "tstr",
        "uint",
        "undefined",
        "unsigned",
        "uri",
    ]

    _controls = [
        ".and",
        ".bits",
        ".cbor",
        ".cborseq",
        ".default",
        ".eq",
        ".ge",
        ".gt",
        ".le",
        ".lt",
        ".ne",
        ".regexp",
        ".size",
        ".within",
    ]

    _re_id = r"""(?x)
        [$@A-Z_a-z]
        (?:[\-\.]*[$@0-9A-Z_a-z]|[$@0-9A-Z_a-z])*
    """
    _re_uint = r"(?:0b[01]+|0x[0-9a-fA-F]+|\d+)"

    flags = re.UNICODE | re.MULTILINE

    tokens = {
        "commentsandwhitespace": [(r"\s+", Text), (r";.+$", Comment.Single)],
        "root": [
            include("commentsandwhitespace"),
            # tag types
            (r"#\d(\.{uint}|)".format(uint=_re_uint), Keyword.Type),
            (r"#", Keyword.Type),  # any
            # occurence
            (
                r"({uint}|)(\*)({uint}|)".format(uint=_re_uint),
                bygroups(Number, Operator, Number),
            ),
            (r"\?|\+", Operator),  # occurrence
            (r"\^", Operator),  # cuts
            (r"(\.\.\.|\.\.)", Operator),  # rangeop
            (words(_controls, suffix=r"\b"), Operator.Word),  # ctlops
            # into choice op
            (r"&(?=\s*({groupname}|\())".format(groupname=_re_id), Operator),
            (r"~(?=\s*{})".format(_re_id), Operator),  # unwrap op
            (r"//|/(?!/)", Operator),  # double und single slash
            (r"=>|/==|/=|=", Operator),
            (r"[\[\]{}\(\),<>:]", Punctuation),
            # Barewords as member keys (must be matched before values, types, typenames, groupnames).
            # Token type is String as barewords are always interpreted as such.
            (
                r"({bareword})(\s*)(:)".format(bareword=_re_id),
                bygroups(String, Text, Punctuation),
            ),
            # predefined types
            (
                words(_prelude_types, prefix=r"(?![\-_$@])\b", suffix=r"\b(?![\-_$@])"),
                Name.Builtin,
            ),
            # user-defined groupnames, typenames
            (_re_id, Name.Class),
            # values
            (r"0b[01]+", Number.Bin),
            (r"0o[0-7]+", Number.Oct),
            (r"0x[0-9a-fA-F]+(\.[0-9a-fA-F]+|)p[+-]?\d+", Number.Hex),  # hexfloat
            (r"0x[0-9a-fA-F]+", Number.Hex),  # hex
            (r"(\d+\.\d+|\d+)(?:e[+-]?\d+|)", Number.Float),
            (r"\d+", Number.Int),
            (r'"(\\\\|\\"|[^"])*"', String),
        ],
    }
