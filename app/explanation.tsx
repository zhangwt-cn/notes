import styles from '../styles/Home.module.scss';

export default function Explanation() {
  return (
    <div className={styles.explanation}>
      <details className={styles.details}>
        <summary>
          <span>About this page</span>
        </summary>
        <p>
          内容来源于 `
          <a
            href="https://github.com/zhangwt-cn/notes"
            target="_blank"
            rel="noreferrer"
          >
            notes
          </a>
          ` 仓库的 issues 和 comments，通过 GitHub API 获取。因使用 GitHub Makrdown 语法，为获得更好体验可以
          <a
            href="https://github.com/zhangwt-cn/notes/issues"
            target="_blank"
            rel="noreferrer noopener"
          >
            <code>点击</code>
          </a>{' '}
          跳转到仓库查看
        </p>
      </details>

      <details className={styles.details}>
        <summary>
          <span>About me</span>
        </summary>

        <p>
          人类最大强大之处在于自我改变。
        </p>
      </details>

      <p>
        <em>
          _💡 如果有任何{' '}
          <a
            href="https://github.com/zhangwt-cn/notes/issues/new"
            target="_blank"
            rel="noreferrer"
          >
            问题或建议
          </a>{' '}
          ，欢迎提出!_
        </em>{' '}
        <br />
        {/* <span className={styles.explanation_notes}>
          Pages take about <b>*300ms~*</b> to fully propagate to the global
          Vercel Edge Network after the regeneration completes.
        </span> */}
      </p>
    </div>
  );
}
