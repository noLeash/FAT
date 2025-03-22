import React from "react";
import { Card as RsCard } from "rsuite"; 
import MarkdownFetcher from "../dashboard/MarkdownFetcher"; // Fetch markdown if needed
import "@/styles/components/dashboard/Card.scss";
import { Accordion, Panel } from 'rsuite'; // ✅ Corrected import

const Card = ({ title, children, footer, markdownFile }) => {
  return (
    <div className="card__title">
      <RsCard className="card">  
        <div className="card__title">
           {title && <RsCard.Header className="card__title">sdf{title}</RsCard.Header>}
        </div>
        <RsCard.Body>
 
              {/* If markdownFile is provided, fetch and display it */}
              
              {markdownFile ? <MarkdownFetcher filename={markdownFile} /> : children}
          
        </RsCard.Body>
        {footer && <RsCard.Footer>{footer}</RsCard.Footer>}
      </RsCard>
    </div>
  );
};

export { Card };
