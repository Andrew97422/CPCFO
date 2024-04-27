import { useEffect, useState, React } from 'react';
import { Form, Container, Row, Button } from 'react-bootstrap';
import axios from 'axios';

import 'bootstrap/dist/css/bootstrap.min.css';

let text_url = "http://localhost:5000/predict_text";
let pdf_url = "http://localhost:5000/predict_pdf";

const headers = {
  'Content-Type': 'application/json'
};


const sendRequest = async (data) => {
  console.log("data = " + data);

  const body = {
    "vacancy": data.toString()
  };

  const response = await axios.post(text_url, body, { headers });
  return response;
};

export default function FormVacancy() {
  const [isLoading, setLoading] = useState(false);
  const [data, setData] = useState("");

  const handleSubmit = async (e) => {
    setLoading(true);
    e.preventDefault();

    if (e.target['txt'].value.trim() !== '') {
      const data1 = e.target['txt'].value.trim();
      const resp = await sendRequest(data1)
      .then((resp) => console.log("response = " + resp.data))
      .then(() => {
        setLoading(false);
      });
    } else if (e.target['pdf'].value.trim() !== '') {
      const data1 = e.target['pdf'].value.trim();
      const resp = await sendRequest(data1)
      .then((resp) => console.log("response = " + resp.data))
      .then(() => {
        setLoading(false);
      });
      console.log("response = " + resp.data);
    }
    setLoading(false);
  };

  const handleClick = () => setLoading(true);

  return (
    <div>
      <Form onSubmit={handleSubmit}>
        <Form.Group className="mb-3">
          <Container>
            <Row>
              <Form.Label id='txt'>
                Вставьте ссылку на вакансию или текст вакансии:
              </Form.Label>
              <br />
              <Form.Control size="lg" type="text" placeholder="URL или текст вакансии" as="textarea" rows={5} id='txt'/>
            </Row>
            <br />
            <Row>
              <Form.Label id='pdf'>Или загрузите PDF вакансии:</Form.Label>
              <br />
              <Form.Control size="lg" type="file" id='pdf'/>
            </Row>
            <br />
          
            <br />
            <Row>
              <Button variant="primary" 
                type="submit"
                disabled={isLoading}
                onClick={!isLoading ? 
                  () => handleClick : null}
              >
                {isLoading ? 'Рекомендации загружаются…' : 'Загрузить рекомендации'}
              </Button>
            </Row>
          </Container>
        </Form.Group>
      </Form>        
    </div>
  )
}
