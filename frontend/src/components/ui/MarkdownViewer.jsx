import React from "react";
import ReactMarkdown from "react-markdown";
import { default as remarkGfm } from "remark-gfm";


const MarkdownViewer = ({ content }) => {
  return (
    <div className="markdown-body p-4 border rounded">
      <ReactMarkdown remarkPlugins={[remarkGfm]}>{content}</ReactMarkdown>
    </div>
  );
};

export default MarkdownViewer;
