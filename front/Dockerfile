FROM node:18.15.0-alpine

WORKDIR /app

# ENV PATH /app/node_modules/.bin:$PATH
COPY public/ /app/public
COPY src/ /app/src
COPY package.json /app/
COPY package-lock.json /app/
RUN npm install --silent
RUN npm install react-scripts@3.4.1 -g --silent

# COPY . ./

EXPOSE 26600

ENV NEXT_TELEMETRY_DISABLED 1
ENV PORT 26600

CMD ["npm", "start"]
