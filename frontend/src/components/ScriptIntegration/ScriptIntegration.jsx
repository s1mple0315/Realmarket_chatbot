import ScriptCopy from "../../icons/ScriptCopy";
import styles from "./ScriptIntegration.module.css";

const ScriptIntegration = () => {
  const phpCode = `<?php
require_once 'config.php';

$link = "https://$subdomain.amocrm.ru/oauth2/access_token";

$data = [
    'client_id'     => $client_id,
    'client_secret' => $client_secret,
    'grant_type'    => 'authorization_code',
    'code'          => $code,
    'redirect_uri'  => $redirect_uri,
];

$curl = curl_init();
curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);
curl_setopt($curl, CURLOPT_USERAGENT, 'amoCRM-oAuth-client/1.0');
curl_setopt($curl, CURLOPT_URL, $link);
curl_setopt($curl, CURLOPT_HTTPHEADER, ['Content-Type:application/json']);
curl_setopt($curl, CURLOPT_HEADER, false);
curl_setopt($curl, CURLOPT_CUSTOMREQUEST, 'POST');
curl_setopt($curl, CURLOPT_POSTFIELDS, json_encode($data));
curl_setopt($curl, CURLOPT_SSL_VERIFYPEER, 1);
curl_setopt($curl, CURLOPT_SSL_VERIFYHOST, 2);
$out = curl_exec($curl);
$code = curl_getinfo($curl, CURLINFO_HTTP_CODE);
curl_close($curl);
$code = (int)$code;
`;

  return (
    <div className={styles.scriptIntegrationContainer}>
      <pre>{phpCode}</pre>
      <ScriptCopy />
    </div>
  );
};

export default ScriptIntegration;
