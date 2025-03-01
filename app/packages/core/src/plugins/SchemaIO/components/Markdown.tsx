import { CopyButton, useTheme } from "@fiftyone/components";
import {
  Box,
  Link,
  Paper,
  SxProps,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Typography,
} from "@mui/material";
import React from "react";
import { useHover } from "react-laag";
import ReactMarkdown from "react-markdown";
import { ReactMarkdownOptions } from "react-markdown/lib/react-markdown";
import { Light as SyntaxHighlighter } from "react-syntax-highlighter";
import js from "react-syntax-highlighter/dist/esm/languages/hljs/javascript";
import python from "react-syntax-highlighter/dist/esm/languages/hljs/python";
import ts from "react-syntax-highlighter/dist/esm/languages/hljs/typescript";
import tomorrow from "react-syntax-highlighter/dist/esm/styles/hljs/tomorrow";
import vs2015 from "react-syntax-highlighter/dist/esm/styles/hljs/vs2015";
import remarkGfm from "remark-gfm";
import styled from "styled-components";

SyntaxHighlighter.registerLanguage("javascript", js);
SyntaxHighlighter.registerLanguage("typescript", ts);
SyntaxHighlighter.registerLanguage("python", python);

const InlineCode = styled.span`
  background: ${({ theme }) => theme.background.level1};
  color: ${({ theme }) => theme.voxel[500]};
  border-radius: 3px;
  padding: 0.2em 0.4em;
  font-size: 85%;
  font-family: Roboto Mono, monospace;
`;

const CodeContainer = styled(Box)`
  border: 1px solid ${({ theme }) => theme.background.level1};
  pre {
    margin: 0;
    padding: 1rem !important;
  }
  border-radius: 3px;
`;

const CodeHeader = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0rem 1rem;
  border-bottom: 1px solid ${({ theme }) => theme.background.level1};
  background: ${({ theme }) => theme.background.level2};
`;

const defaultSx: SxProps = { color: "inherit", mb: 1 };
const boldSx: SxProps = { ...defaultSx, fontWeight: "bold" };

const componentsMap = {
  a({ children, ...props }) {
    if (
      props.href &&
      props.href.startsWith("http") &&
      !props.href.includes(window.location.host)
    ) {
      props = {
        ...props,
        target: "_blank",
      };
    }

    return (
      <Link sx={{ color: "inherit", textDecoration: "underline" }} {...props}>
        {children}
      </Link>
    );
  },
  table({ children }) {
    return (
      <TableContainer component={Paper}>
        <Table>{children}</Table>
      </TableContainer>
    );
  },
  td: TableCell,
  th: TableCell,
  tbody: TableBody,
  thead: TableHead,
  tr: TableRow,
  code({ node, inline, className, children, ...props }) {
    const theme = useTheme();
    const [hovered, hoverProps] = useHover();
    const isDarkMode = theme.mode === "dark";
    const highlightTheme = isDarkMode ? vs2015 : tomorrow;
    const match = /language-(\w+)/.exec(className || "");
    let language = match ? match[1] : "text";
    if (language === "js") {
      language = "javascript";
    }
    if (language === "ts") {
      language = "typescript";
    }
    if (language === "py") {
      language = "python";
    }
    return !inline && match ? (
      <CodeContainer {...hoverProps}>
        <CodeHeader>
          <Typography component="span">{language}</Typography>
          <CopyButton
            text={children}
            sx={{ visibility: hovered ? "visible" : "hidden" }}
          />
        </CodeHeader>

        <SyntaxHighlighter language={language} style={highlightTheme}>
          {children}
        </SyntaxHighlighter>
      </CodeContainer>
    ) : (
      <InlineCode className={className} {...props}>
        {children}
      </InlineCode>
    );
  },
  p: ({ children, ...props }) => (
    <Typography
      sx={{
        color: "inherit",
        "&:not(:first-of-type)": {
          mt: 1,
        },
      }}
    >
      {children}
    </Typography>
  ),
  h1: ({ children, ...props }) => (
    <Typography sx={boldSx} variant="h1" {...props}>
      {children}
    </Typography>
  ),
  h2: ({ children, ...props }) => (
    <Typography sx={boldSx} variant="h2" {...props}>
      {children}
    </Typography>
  ),
  h3: ({ children, ...props }) => (
    <Typography sx={boldSx} variant="h3" {...props}>
      {children}
    </Typography>
  ),
  h4: ({ children, ...props }) => (
    <Typography sx={boldSx} variant="h4" {...props}>
      {children}
    </Typography>
  ),
  h5: ({ children, ...props }) => (
    <Typography sx={boldSx} variant="h5" {...props}>
      {children}
    </Typography>
  ),
  h6: ({ children, ...props }) => (
    <Typography sx={boldSx} variant="h6" {...props}>
      {children}
    </Typography>
  ),
};

export default function Markdown(props: ReactMarkdownOptions) {
  const { children, ...otherProps } = props;

  return (
    <ReactMarkdown
      {...otherProps}
      components={componentsMap}
      remarkPlugins={[remarkGfm]}
    >
      {children}
    </ReactMarkdown>
  );
}
