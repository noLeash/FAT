import React from "react";
import { Card as RsCard } from "rsuite"; // ✅ Avoids conflict

const CardContent = ({ children }) => {
  return <div className="card-content">{children}</div>;
};

const Card = ({ title, children, footer }) => {
  return (
    <RsCard bordered style={{ width: 300 }}>
      {title && <RsCard.Header>{title}</RsCard.Header>}
      <RsCard.Body>
        <CardContent>{children}🫠</CardContent> 
      </RsCard.Body>
      {footer && <RsCard.Footer>{footer}</RsCard.Footer>}
    </RsCard>
  );
};


export { Card, CardContent };
